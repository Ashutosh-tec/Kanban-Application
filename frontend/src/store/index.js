import Vue from 'vue'
import Vuex from 'vuex'
// import VuexPersistence from 'vuex-persist';
// import localForage from 'localforage';
// const vuexLocal = new VuexPersistence({
//   storage: localForage,
//   asyncStorage: true,
// });

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
        // console.log(data)
        // console.log(typeof(data))
      },
      addTask(state, { list_id, data }) {
        state.tasks[`${list_id}`] = data;
        // console.log(data)
        // console.log(state.tasks[`${list_id}`])
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
            const data = await res.json();
            // console.log(data)
            // if (data.length == 0){
            //   context.commit('addLists', [])
            // }else{
            //   context.commit('addLists', data)
            // }
            context.commit("addLists", data);
          } else {
            alert(
              "Something went wrong, Please refresh the page or login again."
            );
          }
        } catch (e) {
          console.log(e);
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
            // console.log(data)
            context.commit("addTask", { list_id, data });
          } else {
            // alert("Something went wrong, Please refresh the page or login again.")
          }
        } catch (e) {
          console.log(e);
        }
      },
    },

    // plugins: [vuexLocal.plugin],

  });
  