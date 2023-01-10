<template>
  <div class="home">
    <!-- <div v-if="localStorage.getItem('auth-token')"> -->
    <NavBar />
    <!-- please use this as image showing reference -->
    <!-- <img alt="Vue logo" src="../assets/logo.png">     -->

    <Home msg="Welcome " />
  <!-- </div> -->

  <!-- <div v-else>
    Please Login first.
  </div> -->

    


  </div>
</template>

<script>
// @ is an alias to /src
import Home from "@/components/Home.vue";
import NavBar from "@/components/NavBar.vue";


export default {
  name: "HomeView",

  components: {
    Home,
    NavBar,

  },

  created: function () {
    this.$store.dispatch("fetchLists");
  },
};
</script>
