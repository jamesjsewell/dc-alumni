Vue.component('profile', {
  template: `<div id='profileContainer' class="row">
	<form id="profileForm" class="form-horizontal col-sm-12" method="POST" action="/profile/api/">
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
		<label for="tag" class="col-sm-2 control-label">Tagline</label>
		<div class="col-sm-9">
		<select v-bind:value="tag" class="form-control" name="tag">
			<option selected="selected" value="Full-stack Engineer">Full-stack Engineer</option>
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
				<label><input v-bind:checked="isActive" type="checkbox" name="isActive" value="">Uncheck here once you've gotten a job to hide your profile.</label>
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
		isActive: true,
		isAdmin: false,
  }},
  created: function() {
    // call database
    axios.get(document.URL + '/api/')
    // axios.get(`http://local.ericmschow.com:8888/profile/api/`)
      .then((response) => {
        this.handleData(response.data)
      })
  },
  methods: {
    handleData: function(data) {
			console.log(data)
			this.fname = data.fname
			this.lname = data.lname
			this.tag = data.tag || 'Full-stack Engineer' // for default since no placeholder on select
			this.email = data.email
			this.description = data.description
			this.github = data.github
			this.linkedin = data.linkedin
			this.resume = data.resume
			this.portfolio = data.portfolio
			this.isAdmin = data.isAdmin
			this.isActive = data.isActive || true // to make checkbox default
    }
  }
})
const app = new Vue({
  el: '#app'
})
