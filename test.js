const { spawn } = require('child_process');
const got = require('got');
const test = require('tape');

// Start the app
const env = Object.assign({}, process.env, {PORT: 5000});
const child = spawn('node', ['index.js'], {env});

test('responds to requests', (t) => {
  t.plan(4);

  // Wait until the server is ready
  child.stdout.on('data', _ => {
    // Make a request to our app
    (async () => {
      const response = await got('http://127.0.0.1:5000');
      // stop the server
      child.kill();
      // No error
      t.false(response.error);
      // Successful response
      t.equal(response.statusCode, 200);
      // Assert content checks
      t.notEqual(response.body.indexOf("<title>Node.js Getting Started on Heroku</title>"), -1);
      t.notEqual(response.body.indexOf("Getting Started on Heroku with Node.js"), -1);
    })();
  });
});

<!-- Project One Row-->
<div class="row justify-content-center no-gutters mb-5 mb-lg-0"> 
    <div class="col-lg-6">
        <!-- <div class="col-xl-12 col-lg-7"> -->
            <div class="mycard">
                <img src="{{ url_for('static', filename='assets/img/bg-masthead.jpg') }}" alt="Avatar" style="width:100%">
                <div class="mycontainer">
                  <h4><b>John Doe</b></h4>
                  <p>Architect & Engineer</p>
                </div>
              </div>
            <!-- <img class="img-fluid mb-3 mb-lg-0" src="{{ url_for('static', filename='assets/img/bg-masthead.jpg') }}" alt="" /> -->
        <!-- </div> -->
    </div>
    <div class="col-lg-6">
        <div class="bg-black text-center h-100 project">
            <div class="d-flex h-100">
                <div class="project-text w-100 my-auto text-center text-lg-left">
                    <h4 class="text-white">Misty</h4>
                    <p class="mb-0 text-white-50">An example of where you can put an image of a project, or anything else, along with a description.</p>
                    <hr class="d-none d-lg-block mb-0 ml-0" />
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Project Two Row-->
<div class="row justify-content-center no-gutters"> 
    <div class="col-lg-6"><img class="img-fluid" src="{{ url_for('static', filename='assets/img/demo-image-02.jpg') }}" alt="" /></div>
    <div class="col-lg-6 order-lg-first">
        <div class="bg-black text-center h-100 project">
            <div class="d-flex h-100">
                <div class="project-text w-100 my-auto text-center text-lg-right">
                    <h4 class="text-white">Mountains</h4>
                    <p class="mb-0 text-white-50">Another example of a project with its respective description. These sections work well responsively as well, try this theme on a small screen!</p>
                    <hr class="d-none d-lg-block mb-0 mr-0" />
                </div>
            </div>
        </div>
    </div>
</div>
