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
        # TODO append tooth code
        query = f"""
        SELECT

        FIRST 1

        c.fullname clients_fullname,

        t.treatdate,
        t.treatcode,
        t.depnum,
        t.mechanic,

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
        AND w.kodoper NOT IN {block_services_codes}
        AND od.schamount_a != 0

        ORDER BY t.treatdate DESC
        """

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
        
        deps.depname,
        
        w.schid,
        w.schname,
        w.kodoper,
        
        CAST(od.schcount AS FLOAT) amount,
        od.schamount_a cost_wo_discount,
        od.schamount cost,
        (od.schamount_a - od.schamount) discount,
        
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
        left join sectorref sec on sec.sectid = t.sectid
        left join sectorref seccl on seccl.sectid = c.sectid
        left join filials f on f.filid = t.filials
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

