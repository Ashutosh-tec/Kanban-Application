<template>
  <div class="bar-chart2">
    <div class="bar-wrapper2">
      <canvas id="myChart2" width="400" height="400"></canvas>
      <label>List vs Task </label>
    </div>
    <div class="bar2-text">
      <h5>List vs Task bar chart compares activity for task in every lists.</h5>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
export default {
  data() {
    return {
      label: [],
      pend_no: [],
      comp_no: [],
    };
  },
  async mounted() {
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/summary_images/3/${localStorage.getItem(
          "user_id"
        )}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      if (res.ok) {
        const data = await res.json();
        this.label = data[0];
        this.pend_no = data[1];
        this.comp_no = data[2];
        // console.log(this.complete_no);
      }
    } catch (e) {
      if (localStorage.getItem("user_id") == null) {
        if (
          confirm("Looks like your account is not detected. Please log in.")
        ) {
          console.log(e);
          this.$router.push("/login");
        }
      }
      console.log(e);
    }

    const ctx2 = document.getElementById("myChart2");

    const myChart2 = new Chart(ctx2, {
      type: "bar",
      data: {
        labels: this.label,
        datasets: [
          {
            label: "Pending Tasks",
            data: this.pend_no,
            backgroundColor: ["rgba(241, 252, 42, 0.8)"],
            borderColor: ["rgba(255, 99, 132, 1)"],
            borderWidth: 1,
          },
          {
            label: "Completed Tasks",
            data: this.comp_no,
            backgroundColor: ["rgba(92, 246, 103, 0.8)"],
            borderColor: ["rgba(25, 99, 132, 1)"],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
    myChart2;
  },
};
</script>

<style>
.bar-wrapper2 {
  display: inline-block;
  position: relative;
  float: right;
  width: 25%;
  height: 25%;
  margin-right: 4rem;
  margin-bottom: 4rem;
  width: 30%;
  height: 30%;
}
.bar2-text {
  margin-top: 5rem;
  padding-top: 5rem;
  font-family: cursive;
}
@media screen and (max-width: 700px) {
  .bar-wrapper2 {
    width: 80%;
    height: 70%;
    float: none;
    margin-bottom: 1rem;
    margin-right: 0rem;
  }
  .bar2-text {
    margin-top: 0rem;
    padding-top: 0rem;
  }
}
</style>
