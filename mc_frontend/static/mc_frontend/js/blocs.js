const progressMessages = {
    'missing-section': {
        'default': {
            'class': 'red',
            'title': 'La section semble manquante',
            'text': 'La section n\'a pas été trouvée. Elle peut être entièrement manquante ou être actuellement une simple sous-section : dans ce cas il vous suffit de corriger le niveau de titre.'
        },
        'section_infrastructure': {
            'class': 'red',
            'title': 'La section semble manquante',
            'text': 'La section n\'a pas été trouvée dans l\'article. D\'après les conventions de style, elle peut être intégrée à la section géographie quand elle est courte. N\'hésitez donc pas à la compléter et à en faire une section à part entière.'
        },
    },
    'many-missing-info': {
        'default': {
            'class': 'red',
            'title': 'Beaucoup d\'informations peuvent manquer',
            'text': 'La section est très brève par rapport aux autres articles comparables. N\'hésitez pas à la compléter.'
        },
    },
    'some-missing-info': {
        'default': {
            'class': 'orange',
            'title': 'Quelques informations peuvent manquer',
            'text': 'La section est d\'une longueur équivalente à celle des autres articles comparables. N\'hésitez cependant pas à la compléter, ainsi qu\'à vérifier le contenu actuel et le mettre à jour le cas échéant.'
        },
    },
    'complete-section': {
        'default': {
            'class': 'green',
            'title': 'Beaucoup d\'informations sont présentes',
            'text': 'La section semble plutôt complète par rapport aux autres articles comparables. N\'hésitez cependant pas à vérifier son contenu, et à le compléter ou le mettre à jour le cas échéant.'
        },
    },  
    'has-main-article': {
        'default': {
            'class': 'green',
            'title': 'La section renvoie à un article détaillé',
            'text': 'La section renvoie à un article détaillé. Vous pouvez consulter ce dernier pour voir s\'il est complet et éventuellement le '
        },
    },
};

const progressLookup = {
    'section_geography': {
        'icon': 'glyphicon glyphicon-tree-conifer',
        'title': 'Géographie',
        'link': 'G.C3.A9ographie',
    },
    'section_history': {
        'icon': 'glyphicon glyphicon-tower',
        'title': 'Histoire',
        'link': 'Histoire',
    },
    'section_economy': {
        'icon': 'glyphicon glyphicon-euro',
        'title': 'Économie',
        'link': '.C3.89conomie',
    },
    'section_demographics': {
        'icon': 'glyphicon glyphicon-user',
        'title': 'Population et société',
        'link': 'Population_et_soci.C3.A9t.C3.A9',
    },
    'section_etymology': {
        'icon': 'glyphicon glyphicon-header',
        'title': 'Toponymie',
        'link': 'Toponymie',
    },
    'section_governance': {
        'icon': 'glyphicon glyphicon-user',
        'title': 'Politique et administration',
        'link': 'Politique_et_administration',
    },
    'section_culture': {
        'icon': 'glyphicon glyphicon-picture',
        'title': 'Culture locale et patrimoine',
        'link': 'Culture_locale_et_patrimoine',
    },
    'section_infrastructure': {
        'icon': 'glyphicon glyphicon-calendar',
        'title': 'Urbanisme',
        'link': 'Urbanisme',
    },
};

macommune.Blocs = function() {
    var blocs = this;
    
    this.init = function() {
        blocs.headerVue = new Vue( {
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
        
        blocs.imagesVue = new Vue( {
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
        
        blocs.progressVue = new Vue( {
            el: '#progress-bloc',
            data: {
                sections_live: {},
                percentages: {},
                averages: {},
                visible: false,
            },
            computed: {
                sections () {
                    var sectionsTable = {};
                    
                    for ( key in this.averages ) {
                        if ( progressLookup[ key ] === undefined ) {
                            continue;
                        }
                        sectionsTable[ key ] = progressLookup[ key ];
                        
                        sectionsTable[ key ][ 'percentage' ] = this.percentages[ key ];
                        sectionsTable[ key ][ 'weight' ] = this.sections_live[ key ];
                        
                        var progress = 'complete-section';
                        if ( sectionsTable[ key ][ 'weight' ] === 0 ) {
                            progress = 'missing-section';
                        }
                        else if ( sectionsTable[ key ][ 'percentage' ] <= 50 ) {
                            progress = 'many-missing-info';
                        }
                        else if ( sectionsTable[ key ][ 'percentage' ] <= 100 ) {
                            progress = 'some-missing-info';
                        }
                        
                        if ( progressMessages[ progress ][ key ] !== undefined ) {
                            sectionsTable[ key ][ 'state' ] = progressMessages[ progress ][ key ];
                        }
                        else {
                            sectionsTable[ key ][ 'state' ] = progressMessages[ progress ][ 'default' ];
                        }
                    }
                    
                    return Object.values( sectionsTable ).sort( function( a, b ) {
                        return a.percentage - b.percentage;
                    } );
                },
            },
            methods: {
                collapseId( section, withHashtag ) {
                    section = section.replace( new RegExp( ' ', 'g' ), '_' );
                    if ( withHashtag ) {
                        return '#collapse' + section;
                    }
                    return 'collapse' + section;
                },
                collapseClasses( index ) {
                    if ( index === 0 ) {
                        return 'panel-collapse collapse in';
                    }
                    return 'panel-collapse collapse';
                },
            },
        } );
    }
    
    this.hideAll = function() {
        blocs.headerVue.visible = false;
        blocs.imagesVue.visible = false;
    };
    
    this.setHeader = function( data ) {
        var wp_last_update = new Date( data.wp_last_update * 1000 );
        
        blocs.headerVue.com_url = 'https://commons.wikimedia.org/wiki/Category:' + data.commons_category;
        blocs.headerVue.nb_anon = data.anoncontributors;
        blocs.headerVue.nb_users = data.registeredcontributors;
        blocs.headerVue.wp_badge = data.wp_article.badge;
        blocs.headerVue.wd_label = data.wd_label;
        blocs.headerVue.wp_length = formatNumber(data.length);
        blocs.headerVue.wp_url = data.wp_article.url;
        blocs.headerVue.wd_url = 'https://www.wikidata.org/wiki/' + blocs.qid;
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
    
    this.setProgress = function( data ) {
        blocs.progressVue.sections_live = data.sections_live;
        blocs.progressVue.percentages = data.percentages;
        blocs.progressVue.averages = data.averages;
        
        blocs.progressVue.$forceUpdate();
        blocs.progressVue.visible = true;
    }
    
    return this.init();
};
