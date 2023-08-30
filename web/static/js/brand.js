class Brand{
    constructor(name, slug, image_url){
        this.name = name;
        this.slug = slug;
        this.image_url = image_url;
    }
}

class Brands{
    constructor() {
        this.collection = [];
        this.concrete_brand = null;
        this.url = '/catalog/brands/';
    }

    get_all(){
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        let brands = $.ajax(
            {
                type: 'get',
                url: this.url,
                headers: {'X-CSRFToken': csrf_token},
                mode: 'same-origin',
                async: false,
                success : function(response)
                {
                    return response;
                },
                error : function(xhr,errmsg,err) {
                    console.log(errmsg);
                }
            }
        )

        brands.responseJSON.forEach((brand) => {
            this.collection.push(
                new Brand(
                    brand.name,
                    brand.slug,
                    brand.file
                )
            )
        })

    }
}


let brands = new Brands()
brands.get_all()
console.log(brands.collection)