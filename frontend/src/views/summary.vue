<template>
  <div>
    <NavBar />
    <!-- <div class="root" style="font-family: 'Alike Angular'; font-size: 22px"> -->
      <h2 style="text-align: center">
        <u>Welcome to summary page of your activity.</u>
      </h2>
      <img src="http://127.0.0.1:5000/api/summary_images/1/1" width="650" height="700">
      <br />
      <br />
      <div class="image">
      <!-- <img :src="require(img2)" alt="Pie chart of tasks" class="img-fluid"> -->
      <BarChart/>
      <PieChart/>
      
        <!-- <img :src="'http://127.0.0.1:5000/api/summary_images/2/' + ids" class="img-circle" alt="Services" />  -->
    
    <!-- </div> -->
    </div>
    <!-- </div> -->
    
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import BarChart from '@/components/BarChart';
import PieChart from '@/components/PieChart.vue';


var ids = localStorage.getItem("user_id");
export default {
  name: "summary_page",
  data() {
    return {
      img1: "http://127.0.0.1:5000/api/summary_images/1/" + ids,
      img2: "http://127.0.0.1:5000/api/summary_images/2/" + ids,
    };
  },
  created: function () {
    if (!localStorage.getItem("user_id")) {
      alert("Please Log in first");
      this.$router.push("/login");
    }
  },
  components: {
    NavBar,
    BarChart,
    PieChart,
  },
};
</script>

<style></style>
