const VUE_APP_DEFS = [
    {
        el: '#vue-library',
        f: () => {import(/* webpackChunkName: "vue-library" */"./views/vue-library")},
    }
];

VUE_APP_DEFS.forEach((appDef) => {
   if (document.querySelector(appDef.el)) {
       appDef.f()
   }
});
