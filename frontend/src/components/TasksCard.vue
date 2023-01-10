<template>
  <div class="root">
    <!-- <h1>Your tasks are here</h1> -->
    <!-- <div v-if="tasks.length == 0">No Tasks to show, Please add one.</div> -->
    <!-- <div v-else> -->

      <div v-for="task in formData" :key="task.task_id">
        <!-- <a>{{ task }}</a> -->
        <div
          class="card"
          style="width: 14rem; margin-top: 10px; "
          :style="[task.task_status == 'Pending'? {'background-color': 'rgb(255, 255, 153)'} : {'background-color': 'rgb(153, 255, 204)'}]"
        >
          <div class="card-header">
            {{ task.task_title }}
          </div>
          <div class="card-body">
            Content : {{ task.task_content }}
            <br />
            Deadline : {{ task.task_deadline }}
            <br />
            Status : {{ task.task_status }}
            <br />
          </div>
          <div class="card-footer">
            
            
  
           
              
            
            <b-dropdown text="List Options" variant="outline-danger" class="m-2">
              <b-dropdown-item 
              type="button"
              class="edBut"
              :to="{
                name: 'edit_task',
                params: { id1: task.list_id, id2: task.task_id },
              }"
              >
                <!-- <router-link
              type="button"
              class="edBut"
              :to="{
                name: 'edit_task',
                params: { id1: task.list_id, id2: task.task_id },
              }"
            > -->
              EDIT
            <!-- </router-link> -->
              </b-dropdown-item>
              <b-dropdown-item 
              type="button"
              class="edBut"
              @click.prevent="deleteTask(task.task_id)"
            >
              DELETE
              </b-dropdown-item>
              
              <b-dropdown-item type="button"
              class="edBut"
              @click.prevent="exportTask(task.task_id)"
              >
                EXPORT
              </b-dropdown-item>
            </b-dropdown>
          </div>
        </div>
      </div>
    <!-- </div> -->
  </div>
</template>

<script>
export default {
  name: "TaskCard",
  props: ["list_id"],
  data() {
    return {
      formData: []
  //     .find(
  //     (ele) => ele.task_id == this.$route.params.id2
  //   ),
    };
  },
  // computed: {
  //   tasks() {
  //     // this.$store.dispatch('fetchTasks', this.list_id);
  //     // console.log(this.$store.state.tasks[`${this.list_id}`])

  //     return this.$store.state.tasks[`${this.list_id}`];
  //   },
  // },
  // created: function () {
    //   location.reload();
    // if (!this.$store.state.tasks[`${this.list_id}`]){
    //   location.reload()
    // }
    // this.getTask()
    // this.$store.dispatch("fetchTasks", this.list_id);
  // },
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
          // console.log(data);
          this.formData = data.filter(
            (ele) => ele.list_id == this.list_id
          );
        }
      } catch (e) {
        console.log(e);
      }
  },
  methods: {
    async deleteTask(task_id) {
      console.log(task_id);
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
          if (res.ok) {
            location.reload();
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
        // const res = await fetch(
        //   `http://127.0.0.1:5000/api/download/list/${list_id}`,
        //   {
        //     method: "get",
        //     headers: {
        //       "Content-Type": "application/json",
        //       "Authentication-Token": localStorage.getItem("auth-token"),
        //     },
        //   }
        // );
        // if (res.ok) {
        // then do whatever

        // location.reload();
        // var url = window.URL.createObjectURL(res.blob());
        //   var a = document.createElement('a');
        //   a.href = url;
        //   a.download = filename;
        //   document.body.appendChild(a);
        //   a.click();
        //   a.remove();
        // download(res.blob())
        // }
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
</style>
