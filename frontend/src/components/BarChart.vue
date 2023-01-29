<template>
  <div class="root-bar">
    <div class="grid" id="bar-wrapper">
      <canvas id="myChart" width="400" height="400"></canvas>
      <label>Date vs Activity </label>
    </div>
    <div class="grid" id="bar-text">
      <h5>This Bar Chart represents overall activity in this app.</h5>
      <a
        >Activity is refering to change you done in your dashbord by creating or
        marking it complete.</a
      >
      <br />
      <div class="para">
        <p v-if="activeCo">
          As the statistics say you have been more actively
          <b
            >Completing Tasks on
            <a v-for="idx in this.effCompIdx" v-bind:key="idx">
              {{ label[idx] }}
            </a></b
          >
        </p>
        <p v-else>
          You have not completed any task yet, but you can start adding and
          completing task now. You can watch your activity on the bar chart.
        </p>
        <p v-if="activeCr">
          You have been more actively
          <b
            >Creating Tasks on
            <a v-for="idx in this.effCreatIdx" v-bind:key="idx">
              {{ label[idx] }}
            </a></b
          >
        </p>
        <p v-else>
          You have not created any task yet, but you can start adding task now.
          You can watch your activity on the bar chart.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  name: "App",

  data() {
    return {
      label: [],
      create_no: [],
      complete_no: [],
      effCompIdx: [], //index completed most tasks
      effCreatIdx: [], //index created most tasks
      activeCr: true,
      activeCo: true,
    };
  },
  async mounted() {
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/summary_images/2/${localStorage.getItem(
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
        this.create_no = data[1];
        this.complete_no = data[2];
        console.log(this.complete_no);
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

    // Calculating Stats of tasks to show on page
    var max = Math.max(...this.create_no);
    console.log(max);
    if (max === 0 || max === -Infinity) {
      this.activeCr = false;
    }
    // console.log(max)
    for (const itm in this.create_no) {
      if (this.create_no[itm] === max) {
        this.effCreatIdx.push(itm);
      }
    }
    var max = Math.max(...this.complete_no);
    if (max === 0 || max === -Infinity) {
      this.activeCo = false;
    }
    // console.log(max)
    for (const itm in this.complete_no) {
      if (this.complete_no[itm] === max) {
        this.effCompIdx.push(itm);
      }
    }
    // End of calculation

    const ctx = document.getElementById("myChart");

    const myChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: this.label,
        datasets: [
          {
            label: "Created Tasks",
            data: this.create_no,
            backgroundColor: ["rgba(241, 252, 42, 0.8)"],
            borderColor: ["rgba(255, 99, 132, 1)"],
            borderWidth: 1,
          },
          {
            label: "Completed Tasks",
            data: this.complete_no,
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
    myChart;
  },
};
</script>

<style>
#bar-wrapper {
  display: inline-block;
  position: relative;
  float: left;
  width: 25%;
  height: 25%;
  margin-left: 4rem;
  margin-bottom: 4rem;
  width: 30%;
  height: 30%;
}

.para {
  font-size: 1.2rem;
  margin-top: 3rem;
}

#bar-text {
  font-family: cursive;
  padding-top: 6rem;
}
@media screen and (max-width: 700px) {
  #bar-wrapper {
    width: 80%;
    height: 70%;
    float: none;
    margin-bottom: 1rem;
  }
  #bar-text {
    padding-top: 0rem;
  }
}
</style>
