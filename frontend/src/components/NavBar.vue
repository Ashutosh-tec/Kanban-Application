<template>
    <nav class="navbar navbar-expand-md bg-dark navbar-dark">
        <a class="navbar-brand" href="/">KANBAN</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="collapsibleNavbar">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link">|</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Summary</a>
            </li>
            <li class="nav-item">
              <a class="nav-link">|</a>
            </li>
            <li class="nav-item">
              <a class="nav-link"
              href=""
              @click.prevent="logout"
              >
                logout
              </a>
              
            </li>    
          </ul>
        </div>  
      </nav>



      <!-- <div id="nav">
        <nav class="container navbar navbar-expand-lg navbar-light bg-light">
          <a class="navbar-brand" href="#">KANBAN</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
              aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
          </button>
      
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <div class="navbar-nav mr-auto">
                  <router-link to="/" class="nav-item nav-link">Home</router-link>
                  <router-link to="/About" class="nav-item nav-link">About</router-link>
                  <router-link to="/Careers" class="nav-link">Careers</router-link>
                  <router-link to="/Contact" class="nav-link">Contact</router-link>
              </div>
              <form class="d-flex">
                  <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                  <button class="btn btn-outline-success" type="submit">Search</button>
              </form>
          </div>
      </nav>
      </div> -->
    
</template>

<script>
export default {
    name: 'NavBar',
    methods: {
    async logout() {
      console.log("Clicked")
      const res = await fetch('http://127.0.0.1:5000/logout')
      if (res.ok) {
        localStorage.clear()
        this.$router.push('/login')
      } else {
        console.log('could not logout the user')
        }
      },
    },
}






</script>

<style>
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
#nav {
  padding: 30px;
  text-align: center;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: whitesmoke;
  background: crimson;
  border-radius: .5rem;
}
</style>