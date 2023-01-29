<template>
  <div class="root board">
    <div class="cards tsk" v-for="task in formData" :key="task.task_id">
      <div
        :style="[
          task.task_status == 'Completed'
            ? { 'background-color': 'rgb(153, 255, 204)' }
            : task.task_deadline < current_date()
            ? { 'background-color': 'rgb(255, 179, 179)' }
            : { 'background-color': 'rgb(255, 255, 153)' },
        ]"
        style="height: 100%"
      >
        <div class="card-header">
          {{ task.task_title }}
        </div>
        <div class="card-body">
          <div class="dropd">
            <b-dropdown
              size="sm"
              text="Options"
              variant="outline-danger"
              class="m-2"
            >
              <b-dropdown-item
                type="button"
                class="edBut"
                :to="{
                  name: 'edit_task',
                  params: { id1: task.list_id, id2: task.task_id },
                }"
              >
                EDIT
              </b-dropdown-item>
              <b-dropdown-item
                type="button"
                class="edBut"
                @click.prevent="deleteTask(task.task_id)"
              >
                DELETE
              </b-dropdown-item>

              <b-dropdown-item
                type="button"
                class="edBut"
                @click.prevent="exportTask(task.task_id)"
              >
                EXPORT
              </b-dropdown-item>
            </b-dropdown>
          </div>

          {{ task.task_content }}

          <br />
          <br />
          Deadline : {{ task.task_deadline }}
          <br />
          Status : {{ task.task_status }}
          <br />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TaskCard",
  props: ["list_id"],
  data() {
    return {
      formData: [],
    };
  },

  async mounted() {
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/user/lists/tasks/${this.list_id}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      if (res.ok) {
        const data = await res.json();
        this.formData = data.filter((ele) => ele.list_id == this.list_id);
      }
    } catch (e) {
      console.log(e);
    }
  },
  methods: {
    current_date() {
      const date = new Date();

      let day = date.getDate();
      if (day < 10) {
        day = "0" + day;
      }
      let month = date.getMonth() + 1;
      if (month < 10) {
        month = "0" + month;
      }
      let year = date.getFullYear();

      // This arrangement can be altered based on how we want the date's format to appear.
      return `${year}-${month}-${day}`;
    },

    async deleteTask(task_id) {
      try {
        if (confirm("Do you really want to delete?")) {
          const res = await fetch(
            `http://127.0.0.1:5000/api/user/lists/tasks/${task_id}`,
            {
              method: "delete",
              headers: {
                "Content-Type": "application/json",
                "Authentication-Token": localStorage.getItem("auth-token"),
              },
            }
          );
          if (res.status == 200) {
            function removeObjectWithId(arr, id) {
              const objWithIdIndex = arr.findIndex((obj) => obj.id === id);
              arr.splice(objWithIdIndex, 1);
              return arr;
            }
            removeObjectWithId(this.formData, task_id);
          } else {
            alert("Something went wrong, please try after refresh your page.");
          }
        }
      } catch (e) {
        console.log(e);
      }
    },
    async exportTask(task_id) {
      try {
        window.open(
          `http://127.0.0.1:5000/api/download/task/${task_id}`,
          "_blank",
          "noreferrer"
        );
      } catch (e) {
        console.log(e);
      }
    },
  },
};
</script>

<style>
.edBut {
  text-decoration: none;
  background: #0d002d2b;
  border: 0cm;
  border-radius: 0.4rem;
  margin: 0.2rem;
  padding: 0.3rem;
  color: rgb(2, 1, 6);
  transition: 0.2s ease-in-out;
}
.edBut:hover {
  color: white;
  background: #0705056b;
  letter-spacing: 0.2rem;
}

.board {
  display: grid;

  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));

  grid-auto-rows: auto;

  grid-gap: 1rem;
}

.tsk {
  border: 2px; /* solid #e7e7e7; */
  border-radius: 4px;
  transition: 0.3s ease-in-out;
  width: 17rem;
  margin-top: 10px;
  padding: 0.5rem;
  font-family: cursive;
}
.tsk:hover {
  width: 19rem;
  font-weight: bold;
  letter-spacing: 0.08rem;
  background-color: rgb(206, 251, 213);
  transition: 0.1s ease-in-out;
}
.dropd {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
