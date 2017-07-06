macommune.Blocs = function() {
    var blocs = this;
    
    this.init = function() {
        blocs.headerVue = new Vue({
            el: '#header-bloc',
            data: {
                visible: false,
                com_url: '',
                nb_anon: 0,
                nb_users: 0,
                wp_badge: '',
                wd_label: '',
                wp_length: 0,
                wp_url: '',
                wd_url: '',
                wv_banner: '',
                wv_url: '',
                wp_last_update: ''
            }
        } );
        
        blocs.imagesVue = new Vue({
            el: '#images-bloc',
            data: {
                visible: false,
                images: [],
                commons_category: '',
                images_number: 0,
                images_in_commons: 9999,
                wp_last_update: ''
            },
            computed: {
                images_number_plural() {
                    return this.images_number > 1 ? 's' : '';
                },
                random_images() {
                    var n = 4,
                        result = new Array( n ),
                        len = this.images.length,
                        taken = new Array( len );
                    if ( n > len )
                        return this.images;
                    while (n--) {
                        var x = Math.floor(Math.random() * len);
                        result[ n ] = this.images[ x in taken ? taken[x] : x ];
                        taken[ x ] = --len;
                    }
                    return result;
                }
            },
        } );
    }
    
    this.hideAll = function() {
        blocs.headerVue.visible = false;
        blocs.imagesVue.visible = false;
    };
    
    this.setHeader = function( data ) {
        var wp_last_update = new Date( data.wp_last_update * 1000 );
        
        blocs.headerVue.com_url = "https://commons.wikimedia.org/wiki/Category:" + data.commons_category;
        blocs.headerVue.nb_anon = data.anoncontributors;
        blocs.headerVue.nb_users = data.registeredcontributors;
        blocs.headerVue.wp_badge = data.wp_article.badge;
        blocs.headerVue.wd_label = data.wd_label;
        blocs.headerVue.wp_length = formatNumber(data.length);
        blocs.headerVue.wp_url = data.wp_article.url;
        blocs.headerVue.wd_url = "https://www.wikidata.org/wiki/" + blocs.qid;
        blocs.headerVue.wv_banner = data.wv_banner;
        blocs.headerVue.wv_url = data.wv_article.url;
        blocs.headerVue.wp_last_update = wp_last_update.toLocaleString();
        
        blocs.headerVue.visible = true;
    };
    
    this.setImages = function( data ) {
        blocs.imagesVue.images = data.images;
        blocs.imagesVue.commons_category = 'https://commons.wikimedia.org/wiki/Special:UploadWizard?categories=' + data.commons_category;
        blocs.imagesVue.images_number = parseInt( data.images_number );
        //blocs.imagesVue.images_in_commons = ... TODO
        
        blocs.imagesVue.visible = true;
    };
    
    return this.init();
};
