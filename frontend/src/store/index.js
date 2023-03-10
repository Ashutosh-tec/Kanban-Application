import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
    strict: true,
    state: {
      lists: [],
      tasks: {},
    },
  
    getters: {
      task(state, list_id, id) {
        console.log(state.tasks[list_id]);
        return state.tasks[list_id].find((ele) => ele.task_id == id);
      },
    },
    mutations: {
      addLists(state, data) {
        state.lists = data;
        
      },
      deleteList(state, id){
        var objWithIdIndex = state.lists.findIndex((obj) => obj.id === id);
        state.lists.splice(objWithIdIndex, 1);
        console.log(JSON.stringify(state.lists))
      },
      addTask(state, { list_id, data }) {
        state.tasks[`${list_id}`] = data;
        
      },
    },
    actions: {
      async fetchLists(context) {
        try {
          const res = await fetch(
            `http://127.0.0.1:5000/api/user/lists/${localStorage.getItem(
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
            console.log(res)
            const data = await res.json();
            context.commit("addLists", data);
          }else if(res.status_code != 200){
            
            console.log("wrong in credentials")
          }
          
          else {
            alert(
              "Something went wrong, Please refresh the page or login again."
            );
          }
        } catch (e) {
          if (confirm("Looks like your account is not detected. Please log in first.")){
          console.log(e);
          router.push("/login");
          }
        }
      },
      async fetchTasks(context, list_id) {
        try {
          const res = await fetch(
            `http://127.0.0.1:5000/api/user/lists/tasks/${list_id}`,
            {
              headers: {
                "Content-Type": "application/json",
                "Authentication-Token": localStorage.getItem("auth-token"),
              },
            }
          );
          if (res.ok) {
            const data = await res.json();
          
            context.commit("addTask", { list_id, data });
          } else {
            alert("Something went wrong, Please refresh the page or login again.")
          }
        } catch (e) {
          console.log(e);
        }
      },
    },

  });
  