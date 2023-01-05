<template>
  <div class="root">
    <!-- <h1>Your tasks are here</h1> -->
    <!-- <div v-if="tasks.length == 0">No Tasks to show, Please add one.</div> -->
    <!-- <div v-else> -->
    <div v-for="task in tasks" :key="task.task_id">
      <!-- <a>{{ task }}</a> -->
      <div
        class="card"
        style="width: 14rem; margin-top: 10px"
        v-bind:style="[
          task.task_status == 'Pending'
            ? 'background-color : rgb(255, 255, 153)'
            : 'background-color : rgb(153, 255, 153)',
        ]"
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
          <router-link
            type="button"
            class="edBut"
            :to="{ name: 'edit_task', params:{id1:task.list_id, id2:task.task_id}}"
          >
            EDIT
        </router-link>
          <button
            type="button"
            class="edBut"
            @click.prevent="deleteTask(task.task_id)"
          >
            DELETE
          </button>
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
  computed: {
    tasks() {
      // this.$store.dispatch('fetchTasks', this.list_id);
      // console.log(this.$store.state.tasks[`${this.list_id}`])
      return this.$store.state.tasks[`${this.list_id}`];
    },
  },
  created: function () {
    this.$store.dispatch("fetchTasks", this.list_id);
    // console.log(this.tasks)//[this.list_id])
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
  },
};
</script>

<style>

.edBut{
  text-decoration: none;
  background: #0d002d2b;
  border: 0cm;
  border-radius: 0.4rem; 
  margin: 0.2rem; 
  padding: 0.3rem;
  color: rgb(2, 1, 6);
  transition: 0.2s ease-in-out;
}
.edBut:hover{
    color: white;
    background: #0705056b;
    letter-spacing: 0.2rem;
}
</style>
