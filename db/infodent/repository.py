import datetime

from db.infodent.db import Connector


class Repository:
    def __init__(self, connector: Connector):
        self.connector: Connector = connector

    @staticmethod
    def map_headings(columns, data) -> list[dict]:
        return [dict(zip(columns, list(row))) for row in data]

    def get_history_treatment(self, lt_date: datetime.date,
                              tooth_code: int, doctor_name: str,
                              block_services_codes: tuple[str],
                              client: str) -> dict:
        if tooth_code == None:
            tooth_code = "null"

        query = f"""
        SELECT

        FIRST 1

        c.fullname clients_fullname,

        t.treatdate,
        t.treatcode,
        t.depnum,
        dm.dname mechanic,

        deps.depname,

        w.schid,
        w.schname,
        w.kodoper,

        CAST(od.schcount AS FLOAT) amount,
        od.schamount_a cost_wo_discount,
        od.schamount cost,
        (od.schamount_a - od.schamount) discount,
        od.toothcode,

        d.dname,
        d.dcode,

        cf.stdtypename doctor_stdtypename,

        f.shortname

        FROM treat t

        left join clients c on c.pcode = t.pcode
        left join clgroup cg on cg.grcod = t.kateg
        left join jpagreement jpa on jpa.agrid = t.jid
        left join jpersons j on j.jid = jpa.jid
        left join doctor d on d.dcode = t.dcode
        left join doctor dm on dm.dcode = t.mechanic
        left join sectorref sec on sec.sectid = t.sectid
        left join sectorref seccl on seccl.sectid = c.sectid
        left join filials f on f.filid = t.filial
        left join jpersons jp on jp.jid = f.jid
        left join treatsch ts on ts.treatcode = t.treatcode
        left join orderdet od on od.orderno = t.orderno and ts.schnum = od.schnum
        left join wschema w on w.schid = od.schcode
        left join doctor dt on dt.dcode = ts.nardcode
        left join departments deps on t.depnum = deps.depnum
        left join conftype cf ON d.stdtype = cf.stdtype

        WHERE 
        t.treatdate <= '{str(lt_date)}' 
        AND d.dname LIKE '%{doctor_name}%' 
        AND c.fullname LIKE '%{client}"%' 
        AND od.toothcode = {tooth_code}
        AND od.schamount_a != 0
        """

        for code in block_services_codes:
            query += f"AND w.kodoper <> '{code}'"

        query += "ORDER BY t.treatdate DESC"

        with self.connector as cursor:
            cursor.execute(query)
            return self.map_headings(
                columns=[column[0] for column in cursor.description],
                data=cursor.fetchall()
            )[0]

    def get_schedule(self, date_begin: datetime.date, date_end: datetime.date) -> list[dict]:
        query = """
        SELECT

        d.dname,
        d.dcode,
        fl.shortname,
        cf.stdtypename doctor_stdtypename,
        sch.beghour,
        sch.endhour,
        deps.depname,
        sch.wdate

        FROM DOCTSHEDULE sch

        LEFT JOIN doctor d ON sch.dcode=d.dcode
        LEFT JOIN conftype cf ON d.stdtype = cf.stdtype
        LEFT JOIN filials fl ON sch.filial=fl.filid
        left join departments deps on sch.depnum = deps.depnum

        WHERE
        sch.wdate BETWEEN '%s' AND '%s'
        """ % (date_begin, date_end)

        with self.connector as cursor:
            cursor.execute(query)
            return self.map_headings(
                columns=[column[0] for column in cursor.description],
                data=cursor.fetchall()
            )

    def get_treatments(self, date_begin: datetime.date, date_end: datetime.date) -> list[dict]:
        query = """
        SELECT
        c.fullname clients_fullname,
        
        t.treatdate,
        t.treatcode,
        t.depnum,
        
        dm.dname mechanic,
        
        deps.depname,
        
        w.schid,
        w.schname,
        w.kodoper,
        
        CAST(od.schcount AS FLOAT) amount,
        od.schamount_a cost_wo_discount,
        od.schamount cost,
        (od.schamount_a - od.schamount) discount,
        od.toothcode,
        
        d.dname,
        d.dcode,
        
        cf.stdtypename doctor_stdtypename,
        
        f.shortname

        FROM treat t
        left join clients c on c.pcode = t.pcode
        left join clgroup cg on cg.grcod = t.kateg
        left join jpagreement jpa on jpa.agrid = t.jid
        left join jpersons j on j.jid = jpa.jid
        left join doctor d on d.dcode = t.dcode
        left join doctor dm on dm.dcode = t.mechanic
        left join sectorref sec on sec.sectid = t.sectid
        left join sectorref seccl on seccl.sectid = c.sectid
        left join filials f on f.filid = t.filial
        left join jpersons jp on jp.jid = f.jid
        left join treatsch ts on ts.treatcode = t.treatcode
        left join orderdet od on od.orderno = t.orderno and ts.schnum = od.schnum
        left join wschema w on w.schid = od.schcode
        left join doctor dt on dt.dcode = ts.nardcode
        left join departments deps on t.depnum = deps.depnum
        left join conftype cf ON d.stdtype = cf.stdtype
        
        WHERE t.treatdate BETWEEN '%s' AND '%s'
        """ % (date_begin, date_end)

        with self.connector as cursor:
            cursor.execute(query)
            return self.map_headings(
                columns=[column[0] for column in cursor.description],
                data=cursor.fetchall()
            )

    def get_month_volume(self, month: int, year: int) -> float:
        query = """
        SELECT 
        
        SUM(od.schamount_a) cost_wo_discount
        
        FROM treat t
        
        left join treatsch ts on ts.treatcode = t.treatcode
        left join orderdet od on od.orderno = t.orderno and ts.schnum = od.schnum

        WHERE extract(month from t.treatdate) = %s AND extract(year from t.treatdate) = %s
        """ % (month, year)

        with self.connector as cursor:
            cursor.execute(query)
            return self.map_headings(
                columns=[column[0] for column in cursor.description],
                data=cursor.fetchall()
            )[0]['COST_WO_DISCOUNT']

    def get_month_volume_payments(self, date_begin: datetime.date, date_end: datetime.date) -> float:
        query = f"""
        select i.pcode, i.extreatcode, i.paydate, i.orderno, iif(i.paycode in (1,3, 5, 8), 'Наличная оплата', 'Авансовый платеж') payname,
        iif(i.paycode in (1, 3, 5), iif(i.paycode in (5, 8), -1 * i.amountrub, i.amountrub), null) cash_amount,
        null ccard_amount,
        iif(i.paycode = 2, i.amountrub, null) avans_amount, null from_avans_amount, null jp_amount,
        c.fullname clients_fullname, c.bdate clients_bdate,
        null jpersons_jname, null jpersons_inn
        from incom i
        left join clients c on i.pcode = c.pcode
        left join doctor d on i.dcode = d.dcode
        left join filials f on i.filial = f.filid
        left join cashref cash on i.cashid = cash.cashid
        where (i.paydate between '{date_begin}' and '{date_end}')
        and (i.paycode in (1, 2, 3, 5, 8))
         -- 1 оплата приема
         -- 2 авансовый платеж
         -- 3 оплата долга
         -- 5,8 возврат
        and (-1 in (-1) or f.filid in (-1))
        and (-1 in (-1) or cash.cashid in (-1))
        union all
        select j.pcode, j.treatcode, j.pmdate, null,
        iif(j.bnalpay = 1, 'Безналичная оплата', 'Банковская карта'),
        null cash_amount,
        iif(a.credcard = 1  and (j.bnalpay is null or j.bnalpay = 0), iif(j.opertype in (5, 8), -1 * j.amountrub, j.amountrub), null)  ccard_amount,
        null avans_amount, null from_avans_amount,
        iif(j.bnalpay = 1, iif(j.opertype in (5, 8), -1 * j.amountrub, j.amountrub), null) jp_amount,
        c.fullname clients_fullname, c.bdate clients_bdate,
        null, null
        from jppayments j
        left join clients c on j.pcode = c.pcode
        left join doctor d on j.dcode = d.dcode
        left join filials f on j.filial = f.filid
        left join cashref cash on j.cashid = cash.cashid
        left join jpagreement a on j.agrid = a.agrid
        left join jpersons jp on jp.jid = a.jid
        where j.pmdate between '{date_begin}' and '{date_end}'
        and j.opertype in (1, 5, 8)
        and (a.credcard = 1  and (j.bnalpay is null or j.bnalpay = 0)  -- кредитная карта
        or j.bnalpay = 1)
        and (-1 in (-1) or f.filid in (-1))
        and (-1 in (-1) or cash.cashid in (-1))
        union all
        select t.pcode, t.treatcode, t.treatdate, o.orderno, 'Безналичная оплата',
        null cash_amount,
        null ccard_amount,
        null avans_amount, null from_avans_amount,
        sum(o.schamount) jp_amount,
        max(c.fullname) fullname, max(c.bdate) bdate,
        max(jp.jname) jpersons_jname, max(jp.jinn) jpersons_inn
        from treat t
        left join jpagreement jpa on t.jid = jpa.agrid
        left join jpersons jp on jp.jid = jpa.jid
        left join clients c on c.pcode = t.pcode
        left join orderdet o on o.orderno = t.orderno
        where treatdate between '{date_begin}' and '{date_end}'
        and o.doctype = 11
        and (-1 in (-1) or t.filial in (-1))
        and (-1 in (-1) or t.cashid in (-1))
        group by t.pcode, t.treatcode, t.treatdate, o.orderno
        union all
        -- погашение из аванса
        select
        cl.pcode, null, cl.paydate, null,
        'Погашение из аванса',
        null cash_amount,
        null ccard_amount,
        null avans_amount, cl.amountrub from_avans_amount, null jp_amount,
        c.fullname clients_fullname, c.bdate clients_bdate,
        null jpersons_jname, null jpersons_inn
        from clavans cl
        left join clients c on c.pcode = cl.pcode
        left join clavanstype cla on cl.avanstype = cla.avanstype
        left join doctor d on cl.dcode = d.dcode
        left join filials f on cl.filial = f.filid
        left join cashref cash on cl.cashid = cash.cashid
        left join treat t on (cl.pcode = t.pcode and cl.treatcode = t.treatcode)
        where cl.paydate >= '{date_begin}'  and cl.paydate <= '{date_end}'
        and cl.treatcode is not null and cl.typeoper = 1
        and (-1 in (-1) or cl.filial in (-1))
        and (-1 in (-1) or cl.cashid in (-1))
        union all
        -- погашение долга из аванса
        select l.pcode, null, l.lcdate, null,
        'Погашение долга из аванса',
        null cash_amount,
        null ccard_amount,
        null avans_amount, l.amountrub from_avans_amount, null jp_amount,
        c.fullname clients_fullname, c.bdate clients_bdate,
        null jpersons_jname, null jpersons_inn
        from losecredit l
        left join clients c on c.pcode = l.pcode
        left join treat t on (l.treatcode = t.treatcode)
        left join clavans a on (l.avansid = a.id)
        left join clavanstype cla on a.avanstype = cla.avanstype
        left join doctor d on l.dcode = d.dcode
        left join filials f on l.filial = f.filid
        left join cashref cash on l.cashid = cash.cashid
        where l.lcdate >= '{date_begin}' and l.lcdate <= '{date_end}'
        and l.paycode = -2
        and (-1 in (-1) or l.filial in (-1))
        and (-1 in (-1) or l.cashid in (-1))
        --order by  11, 1, 3
        order by  11, 1, 3
        """

        with self.connector as cursor:
            cursor.execute(query)
            payments = self.map_headings(
                columns=[column[0] for column in cursor.description],
                data=cursor.fetchall()
            )
            total = 0
            for pay in payments:
                total += pay['CASH_AMOUNT'] or 0
                total += pay['CCARD_AMOUNT'] or 0
                total += pay['AVANS_AMOUNT'] or 0

            return total
