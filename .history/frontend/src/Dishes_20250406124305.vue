<script>

export default{
  name:'Dishes',
  components:{

  },
  setup(){

    //data
    const dishes = ref([]);
    //methods

    //computed

    //watch

    //Хуки
  }
}
</script>

<template>
    <div class="dishes-container">
    <h2>Список блюд:</h2>
    <ul class="dish-items-list">
        <li v-for="(dish,index) in dishes ":key="index" class="dish-item">
            <ul>
          <li v-for="(ingredient, idx) in dish.ingredients" :key="idx">
            {{ ingredient }}
          </li>
        </ul>
        </li>
    </ul>
</div>
</template>

<style scoped>

</style>
