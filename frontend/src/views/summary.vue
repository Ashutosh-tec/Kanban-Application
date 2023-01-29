<template>
  <div class="root">
    <NavBar />
    <h2 style=" font-family: 'Lucida Console';">
      <u>Summary of your activity.</u>
    </h2>
    <br />
    <br />
    <div class="image">
      <BarChart />
      
      <br />
      <br />
      <br />
      <BarChart2/>
      <br />
      <br />
      <br />

      <PieChart/>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import BarChart from "@/components/BarChart";
import PieChart from "@/components/PieChart.vue";
import BarChart2 from "@/components/BarChart2.vue";

export default {
  name: "summary_page",
  data() {
    return {

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
    BarChart2,
  },
};
</script>

<style>
.root{
  text-align: center;
}
</style>
