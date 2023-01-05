<template>
  <div class="home">
    <NavBar />
    <!-- please use this as image showing reference -->
    <!-- <img alt="Vue logo" src="../assets/logo.png">     -->
    <Home msg="Welcome " />
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
