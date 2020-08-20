// let tokenUrl = window.location.href.match(/\#(?:access_token)\=([\S\s]*?)\&/);

// console.log('js tokenzzz 1111 ::: ', tokenUrl);
var token = "";
var payload = "";
var tokenUrl = "";
const JWTS_LOCAL_KEY = "JWTS_LOCAL_KEY";
const JWTS_ACTIVE_INDEX_KEY = "JWTS_ACTIVE_INDEX_KEY";

$(function () {
  //   var tokenUrl = window.location.href.match(/[^\/]+$/);
  tokenUrl = window.location.hash.substr(1).split("&")[0].split("=");
  console.log('im token ', tokenUrl)
  check_token_fragment();
  let token = tokenUrl[1];
  console.log("token: ", token);
  console.log("tokenUrl: ", tokenUrl);
  localStorage.setItem("token", token);
  if (token === null) {
    hideOnLogin();
  } else {
    // try {
    //   let permissions;
    //   permissions = JSON.parse(atob(token.split(".")[1])).permissions;
    //   localStorage.setItem("permissions", permissions);
    //   console.log("permissions: ", permissions);
    //   if (!localStorage.getItem("permissions")) {
    //     permissions = ["read:movies", "read:actors"]; // default permissions
    //     localStorage.setItem("permissions", permissions);
    //   }
    // } catch (e) {
    //   console.log("E: ", e);
    // }
    hideOnLogin();
    sendData();
  }
});

const sendData = async (url, data, method) => {
  // Default options are marked with *
  const response = await fetch(url, {
    method, // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: new Headers({
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    }),
    redirect: "follow", // manual, *follow, error
    referrer: "no-referrer", // no-referrer, *client
    // body: JSON.stringify(data) // body data type must match "Content-Type" header
    body: data,
  });
  console.log("ressssiii: ", response);

  return await response.json(); // parses JSON response into native JavaScript objects
};
function hideOnLogin() {
  console.log("yess ", localStorage.getItem("permissions"));
  if (
    (localStorage.getItem("token") && localStorage.getItem("permissions")) !==
    null
  ) {
    hideSign_inup();
    if (localStorage) {
      //if local storage
      if (!localStorage.getItem("loggedIn")) {
        hideView_AM();
      }
    }
  } else if (
    localStorage.getItem("token") &&
    localStorage.getItem("permissions") === null
  ) {
    hideView_AM();
    if (localStorage) {
      //if local storage
      if (!localStorage.getItem("loggedOut")) {
        hideSign_inup();
      }
    }
    // document.getElementById("ManageCasting").remove();
  }
}
function hideSign_inup() {
  console.log("here i am ");
  document.getElementById("ManageCastingtitle").innerHTML = "Manage Casting";
  document.getElementById("about_in_login").remove();
  document.getElementById("about").remove();
  document.getElementById("signin_signup").remove();
  document.getElementById("loginBtn").remove();
  // document.getElementById("signUpBtn").remove();
  localStorage.setItem("loggedIn", true);
}
function hideView_AM() {
  console.log("here i am 2");
  document.getElementById("ManageCastingtitle").innerHTML =
    "login or signup to Manage Casting";

  document.getElementById("logoutBtn").remove();
  document.getElementById("ViewMoviez").remove();
  document.getElementById("viewActorz").remove();
  document.getElementById("hideViewActors").remove();
  document.getElementById("hideViewMovies").remove();
  localStorage.setItem("loggedOut", true);
}

function check_token_fragment() {
  // parse the fragment
  const fragment = tokenUrl; //window.location.hash.substr(1).split("&")[0].split("=");
  // check if the fragment includes the access token
  if (fragment[0] === "access_token") {
    // add the access token to the jwt
    this.token = fragment[1];
    console.log("test::::::: ========== ", this.token);
    localStorage.setItem("token", this.token);
    // save jwts to localstore
    this.set_jwt();
  }
}

function set_jwt() {
  localStorage.setItem(JWTS_LOCAL_KEY, this.token);
  if (this.token) {
    this.decodeJWT(this.token);
  }
}

function load_jwts() {
  this.token = localStorage.getItem(JWTS_LOCAL_KEY) || null;
  if (this.token) {
    this.decodeJWT(this.token);
  }
}

function activeJWT() {
  return this.token;
}

function decodeJWT(token) {
  //   const jwtservice = new JwtHelperService();
  //   this.payload = jwtservice.decodeToken(token);
  //   return this.payload;
  var base64Url = token.split(".")[1];
  var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  var jsonPayload = decodeURIComponent(
    atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );
  console.log("JSON:::: ", JSON.parse(jsonPayload));
  this.payload = JSON.parse(jsonPayload);
  localStorage.setItem("permissions", this.payload.permissions);

  // var setsession = window.sessionStorage.setItem("animals", this.payload);
  // var getsession = window.sessionStorage.getItem("animals");
  // console.log("getsession ", getsession);
  return this.payload;
}

const logOut = () => {
  this.token = "";
  this.payload = null;
  this.set_jwt();
  localStorage.clear();
  window.location.href = "https://fsndy.auth0.com/v2/logout";
};
