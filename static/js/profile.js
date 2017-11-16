Vue.component('profile', {
  template: `<div id='profileContainer' class="row">
	<form id="profileForm" class="form-horizontal col-sm-12" method="POST" action="/api/student/">
	<h2 class="text-center">Your Profile</h2>
  <div class="form-group">
    <label for="fname" class="col-sm-2 control-label">Full Name</label>
    <div class="col-sm-4">
			<input v-bind:value="fname" type="text" class="form-control" name="fname" placeholder="First Name">
		</div>
		<div class="col-sm-5">
	    <input v-bind:value="lname" type="text" class="form-control" name="lname" placeholder="Last Name">
		</div>
  </div>
  <div class="form-group">
    <label for="email" class="col-sm-2 control-label">Email</label>
    <div class="col-sm-9">
      <input v-bind:value="email" type="email" class="form-control" name="email" placeholder="Email address">
    </div>
  </div>
  <div class="form-group">
    <label for="linkedin" class="col-sm-2 control-label">LinkedIn</label>
    <div class="col-sm-9">
      <input v-bind:value="linkedin" type="text" class="form-control" name="linkedin" placeholder="Link to your LinkedIn account.">
    </div>
  </div>
	<div class="form-group">
    <label for="github" class="col-sm-2 control-label">GitHub</label>
    <div class="col-sm-9">
      <input v-bind:value="github" type="text" class="form-control" name="github" placeholder="Link to your GitHub account.">
    </div>
  </div>
	<div class="form-group">
		<label for="portfolio" class="col-sm-2 control-label">Portfolio</label>
		<div class="col-sm-9">
			<input v-bind:value="portfolio" type="text" class="form-control" name="portfolio" placeholder="Link to your personal portfolio.">
		</div>
	</div>
	<div class="form-group">
		<label for="resume" class="col-sm-2 control-label">Resume</label>
		<div class="col-sm-9">
			<input v-bind:value="resume" type="text" class="form-control" name="resume" placeholder="Link to your resume, hosted on your portfolio.">
		</div>
	</div>
	<div class="form-group">
		<label for="tag" class="col-sm-2 control-label">Tag</label>
		<div class="col-sm-9">
		<select v-bind:value="tag" class="form-control" name="tag">
			<option value="Full-stack Engineer">Full-stack Engineer</option>
			<option value="Front-end Engineer">Front-end Engineer</option>
			<option value="Back-end Engineer">Back-end Engineer</option>
			<option value="Web Developer">Web Developer</option>
		</select>
		</div>
	</div>
	<div class="form-group">
		<label for="description" class="col-sm-2 control-label">Description</label>
		<div class="col-sm-9">
			<textarea v-bind:value="description" class="form-control" rows="5" name="description" placeholder="Put your elevator pitch here."></textarea>
		</div>
	</div>
  <div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
			<div class="checkbox">
				<label><input v-bind:value="isActive" type="checkbox" name="isActive" checked value="">Uncheck here once you've gotten a job to hide your profile.</label>
			</div>
		</div>
	</div>
	<div class="form-group">
		<div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-primary">Save Changes</button>
    </div>
  </div>
</form>
    </div>`,
  data: function() {return {
		fname: '',
		lname: '',
		tag: '',
		email: '',
		description: '',
		linkedin: '',
		github: '',
		resume: '',
		portfolio: '',
		isActive: false,
		isAdmin: false,
  }},
  created: function() {
    // call database
    axios.get(`http://local.ericmschow.com:8888/api/student/`)
      .then((response) => {
        this.handleData(response.data)
      })
  },
  methods: {
    handleData: function(data) {
			console.log(data)
			this.fname = data.fname
			this.lname = data.lname
			this.tag = data.tag
			this.email = data.email
			this.description = data.description
			this.github = data.github
			this.linkedin = data.linkedin
			this.resume = data.resume
			this.portfolio = data.portfolio
			this.isAdmin = data.isAdmin
			this.isActive = data.isActive
    }
  }
})
Vue.component('alum', {
  template: `
<div class='alum'>
  <h4>{{student.fname.toUpperCase()}} {{student.lname.toUpperCase()}}</h4>
  <h6>{{student.tag.toUpperCase()}}</h6>
  <hr class='green1'>
  <p>{{student.description}}</p>
  <hr class='green1'>
  <div class='row icons'>
    <a :title=githubtitle :href=github target="_blank"><i class="fa fa-github" aria-hidden="true"></i></a>
    <a :title=linkedintitle :href=linkedin target="_blank"><i class="fa fa-linkedin" aria-hidden="true"></i></a>
    <a :title=resumetitle :href=resume target="_blank"><i class="fa fa-file-text-o" aria-hidden="true"></i></a>
    <a :title=portfoliotitle :href=portfolio target="_blank"><i class="fa fa-file-code-o" aria-hidden="true"></i></a>
  </div>
</div>`,
  props: {student: Object, arrlength: Number },
	// data() {return {student: this.student, arrlength: this.arrlength}},
  created: function() {
    console.log('alum created', this.student, this.arrlength)
  },
  computed: {
    github: function() {
      return (this.student.github)
    },
    linkedin: function() {
      return (this.student.linkedin)
    },
    resume: function() {
      return (this.student.resume)
    },
    portfolio: function() {
      return (this.student.portfolio)
    },
    githubtitle: function() {
      return ('' + this.student.name + "'s GitHub Account")
    },
    linkedintitle: function() {
      return ('' + this.student.name + "'s LinkedIn Account")
    },
    resumetitle: function() {
      return ('' + this.student.name + "'s Resume")
    },
    portfoliotitle: function() {
      return ('' + this.student.name + "'s Personal Website and Portfolio")
    }
  }
})

// var app = new Vue({
//   el: '#app',
// })
const app = new Vue({
  el: '#app'
})
