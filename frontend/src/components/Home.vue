<template>
  <div class="hello">
    <h1>{{ msg }}{{ user }}</h1>
    <a>{{ lists }}</a>
    
    <div v-for="list in lists" :key="list.list_id">
      <div class="card" style="width: 15rem; margin-top: 2rem">
        <div class="card-header">
          <a>List Name: </a> <b>{{ list.list_name }}</b>
          
          
          <div style="float: right;">
            <b-dropdown size="lg"  variant="link" toggle-class="text-decoration-none" no-caret style="margin: -2rem;">
              <template #button-content>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-list" viewBox="0 0 16 16">
                  <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"/>
                </svg>
              </template>
              <b-dropdown-item class="edBut" type="button"
            style="margin: 0.1rem;"
            :to="{ name: 'edit_list', params:{id:list.list_id}}"
          >
            Edit
              </b-dropdown-item>
              <b-dropdown-item class="edBut" type="button" @click.prevent="deleteList(list.list_id)">
                Delete
              </b-dropdown-item>
              <b-dropdown-item  class="edBut" type="button" @click.prevent="exportList(list.list_id)"> 
                Export 
         
              </b-dropdown-item>
            </b-dropdown>
          </div>
        
        </div>
        <!-- <ul class="list-group list-group-flush"> -->
          <!-- <li class="list-group-item">
            <div class="dropdown">
              <button>List Options</button>
              <div class="dropdown-content">
                <a href="/todos/#">Edit</a>
                <a href="/todos/#">Delete</a>
              </div>
            </div>
          </li> -->
          <!-- <li class="list-group-item" style="padding: 0.1rem">
            
             <div>
              <b-dropdown id="dropdown-1" text="List Options" class="m-md-2">
                
              
              </b-dropdown>
            </div>
          
          </li>
        </ul> -->
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
    async exportList(list_id){
      try {
        window.open(`http://127.0.0.1:5000/api/download/list/${list_id}`, '_blank', 'noreferrer');
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
          // then do what you want
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
