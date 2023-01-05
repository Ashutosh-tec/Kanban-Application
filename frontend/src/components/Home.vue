<template>
  <div class="hello">
    <h1>{{ msg }}{{ user }}</h1>
    <a>{{ lists }}</a>
    <div v-for="list in lists" :key="list.list_id">
      <div class="card" style="width: 12rem; margin-top: 2rem">
        <div class="card-header">
          <a>List Name: </a> <b>{{ list.list_name }}</b>
        </div>
        <ul class="list-group list-group-flush">
          <!-- <li class="list-group-item">
            <div class="dropdown">
              <button>List Options</button>
              <div class="dropdown-content">
                <a href="/todos/#">Edit</a>
                <a href="/todos/#">Delete</a>
              </div>
            </div>
          </li> -->
          <li class="list-group-item" style="padding: 0.1rem">
            <router-link
              class="btn btn-dark edtbtn"
              style="margin: 0.1rem;"
              :to="{ name: 'edit_list', params:{id:list.list_id}}"
            >
              Edit
            </router-link>
            <button class="btn btn-dark" @click.prevent="deleteList(list.list_id)">Delete</button>
          </li>
        </ul>
      </div>
      <div class="card" style="background-color: azure">
        <!-- <div class="card-header">
          {{ list.list_name }}
        </div> -->

        <div class="card-body">
          <!-- <h5 class="card-title">Special title treatment</h5>
          <p class="card-text">
            With supporting text below as a natural lead-in to additional
            content.
          </p> -->
          <TasksCard v-bind:list_id="list.list_id" />
          <router-link
            class="btn btn-primary"
            :to="{ name: 'add_task', params:{id:list.list_id}}"
            >Add Task</router-link
          >
        </div>
      </div>
    </div>
    <!-- <div class="card">
      <img alt="Click Here to Add List" src="../assets/sign-add-icon.jpeg" />
      <span>Add List</span>
    </div> -->
    <div class="card" style="width: 8rem; height: 8rem">
      <!-- <a href="/add_list"> -->
        <router-link :to="{name:'add_list'}">
        <img alt="Click Here to Add List" src="../assets/sign-add-icon.jpeg" />
        <div class="card-body">
          <h5 class="card-text">Add List</h5>
          <!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
        </div>
      </router-link>
      <!-- </a> -->
    </div>
  </div>
</template>

<script>
import TasksCard from "./TasksCard.vue";
export default {
  name: "HelloWorld",
  data() {
    return {
      user: localStorage.getItem("username"),
    };
  },
  props: {
    msg: String,
  },
  components: {
    TasksCard,
  },
  computed: {
    lists() {
      // console.log(this.$store.state.lists)
      return this.$store.state.lists;
    },
  },
  methods: {
    editList(list_id) {
      this.$router.push(`/edit_list/${list_id}`);
    },
    async deleteList(list_id){
      try {
        if (confirm("Do you really want to delete?")) {
          const res = await fetch(
            `http://127.0.0.1:5000/api/user/lists/${list_id}`,
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.dropdown {
  display: inline-block;
  position: relative;
}
.dropdown-content {
  display: none;
  position: absolute;
  width: 100%;
  overflow: auto;
  box-shadow: 0px 10px 10px 0px rgba(0, 0, 0, 0.4);
}
.dropdown:hover .dropdown-content {
  display: block;
}
.dropdown-content a {
  display: block;
  color: #000000;
  padding: 0.02px;
  text-decoration: none;
}
.dropdown-content a:hover {
  color: #ffffff;
  background-color: #00a4bd;
}
.edtbtn{
  text-decoration: none;
  color: white;
}
</style>
