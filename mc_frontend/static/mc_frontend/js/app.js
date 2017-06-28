Vue.component('page-header', {
    template: `<div class="page-header">
      <h1 id="article-title">{{ wd_label }}</h1>
      <div style="float: right;">
        <ul>
          <li><a v-bind:href="wp_url">Wikipédia</a></li>
          <li><a v-bind:href="com_url">Wikimedia Commons</a></li>
          <li><a v-bind:href="wd_url">Wikidata</a></li>
          <li><a v-bind:href="wv_url">Wikivoyage</a></li>
        </ul>
      </div>
      <div class="base-info">
        <ul>
          <li>Dernière modification de la page : {{ updated }}</li>
          <li>Taille de la page (en octets) : {{wp_weight }}</li>
          <li>Nombre de contributeurs enregistrés : {{ nb_users }}</li>
          <li>Nombre de contributeurs anonymes : {{ nb_anon }}</li>
        </ul>
      </div>
    </div>`,
    props: ['com_url',
            'nb_anon',
            'nb_users',
            'updated',
            'wd_url',
            'wd_label',
            'wp_badge',
            'wp_weight',
            'wp_url',
            'wv_url']
});
