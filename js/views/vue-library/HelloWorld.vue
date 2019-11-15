<template>
    <div>
        <h1>Hello World!</h1>
    </div>
</template>

<script lang="ts">
    import Vue from "vue";
    import {Component} from "vue-property-decorator";

    @Component({})
    export default class HelloWorld extends Vue {

    }
</script>

<style scoped lang="sass">
    h1
        color: red
</style>
