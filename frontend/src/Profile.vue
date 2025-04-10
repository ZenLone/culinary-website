<script>
import TrueAuth from './components/trueAuth.vue';
import trueAuth from './components/trueAuth.vue';
import falseAuth from './components/falseAuth.vue';
export default{
    name:'Profile',
    components:{
    trueAuth,
    falseAuth
    },
    setup(){
        //data

        //methods

        //Хуки
    }
}
</script>
<template>
<!-- <trueAuth></trueAuth> -->
 <falseAuth></falseAuth>
</template>
<style scoped>

</style>