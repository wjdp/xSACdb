import HelloWorld from './HelloWorld.vue';
import Vue from 'vue';

new Vue({
    el: '#vue-library',
    components: {
        HelloWorld,
    },
    template: '<HelloWorld/>'
});
