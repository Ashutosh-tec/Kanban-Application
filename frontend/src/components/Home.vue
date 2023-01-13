<template>
  <div class="hello" style="width:100%">
    <h1> {{ msg }}{{ user }},</h1>
    <!-- <a>{{ lists }}</a> -->

    <div v-for="list in lists" :key="list.list_id">
      <div class="cards" style="width: 18rem;height:3.2rem; margin-top: 2rem">
        <div class="card-header">
          <a>Name: </a> <b>{{ list.list_name }}</b>

          <div style="float: right">
            <b-dropdown
              size="lg"
              variant="outline-danger"
              toggle-class="text-decoration-none"
              no-caret
              style="margin: -2rem"
            >
              <template #button-content>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  fill="currentColor"
                  class="bi bi-list "
                  viewBox="0 0 16 16"
                  
                >
                  <path
                    fill-rule="evenodd"
                    d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"
                  />
                </svg>
              </template>
              <b-dropdown-item
                type="button"
                class="edBut"
                style="margin: 0.1rem"
                :to="{ name: 'edit_list', params: { id: list.list_id } }"
              >
                EDIT 
              </b-dropdown-item>
              <b-dropdown-item
                class="edBut"
                type="button"
                @click.prevent="deleteList(list.list_id)"
              >
                DELETE 
              </b-dropdown-item>
              <b-dropdown-item
                class="edBut"
                type="button"
                @click.prevent="exportList(list.list_id)"
              >
                EXPORT 
              </b-dropdown-item>
            </b-dropdown>
          </div>
          
        </div>
        
      </div>
      <div class="card mainboard" >
        <!-- <div class="card-header">
          {{ list.list_name }}
        </div> -->

        <div class="card-body bdy">
          <!-- <h5 class="card-title">Special title treatment</h5>
          <p class="card-text">
            With supporting text below as a natural lead-in to additional
            content.
          </p> -->
          <TasksCard v-bind:list_id="list.list_id" />
          <router-link
            class="edBut addTask"
            :to="{ name: 'add_task', params: { id: list.list_id } }"
            >
            Add Task
            </router-link
          >
          <br/>
          
        </div>
      </div>
    </div>
    <!-- <div class="card">
      <img alt="Click Here to Add List" src="../assets/sign-add-icon.jpeg" />
      <span>Add List</span>
    </div> -->
    <div style="display: flex;justify-content: center;
    align-items: center;">
    <b-button block variant="outline-secondary" v-b-modal.list-modal style="width:70%; margin:1rem; font-size:1.5em">
      
      Add List
    </b-button>
      </div>
    <AddListComp />
  </div>
</template>

<script>
import TasksCard from "./TasksCard.vue";
import AddListComp from "./AddListComp.vue";
export default {
  name: "HelloWorld",
  data() {
    return {
      user: localStorage.getItem("username"),
      arr: [],
      // list_id: null,
    };
  },
  props: {
    msg: String,
  },
  components: {
    TasksCard,
    AddListComp,
  },
  computed: {
    lists() {
      // console.log(this.$store.state.lists)
      sessionStorage.setItem('lists',JSON.stringify(this.$store.state.lists))
      return this.$store.state.lists;
    },
  },

  methods: {
    // record(id){
    //   this.list_id = id
    // },
    editList(list_id) {
      this.$router.push(`/edit_list/${list_id}`);
    },
    async deleteList(list_id) {
      try {
        if (confirm("All tasks inside this list will be deleted. Do you still want to delete?")) {
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
          if (res.status == 200) {
            // function removeObjectWithId(arr, id) {
            //   const objWithIdIndex = arr.findIndex((obj) => obj.id === id);
            //   arr.splice(objWithIdIndex, 1);
            //   return arr;
            // }
            // removeObjectWithId(this.lists, list_id);
            this.$store.commit("deleteList", list_id)
            // location.reload();
          } else{
            alert("Something went wrong, please try after refresh your page.")
          }
        }
      } catch (e) {
        console.log(e);
      }
    },
    async exportList(list_id) {
      try {
        window.open(
          `http://127.0.0.1:5000/api/download/list/${list_id}`,
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
.addTask{
  font-size:2em;
  background: #2114ae2b;
  border: 0.1rem solid black;
  border-radius: 0.4rem;
}
.edBut:hover {
  color: white;
  background: #0705056b;
  letter-spacing: 0.2rem;
}
.btn { /*one reference is inside list menu button*/
 
    padding: -0.5rem 0.9re
}
.mainboard{
  background-color: azure;
  transition: 0.2s ease-in-out;
}
.mainboard:hover{
  background-color: rgb(222, 252, 227);
}

.bdy{
  padding-top:0.25rem
}
</style>
