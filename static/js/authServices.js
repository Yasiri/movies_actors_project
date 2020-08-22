// let tokenUrl = window.location.href.match(/\#(?:access_token)\=([\S\s]*?)\&/);
var token = "";
var payload = "";
var tokenUrl = "";
let permissions;
const JWTS_LOCAL_KEY = "JWTS_LOCAL_KEY";
const JWTS_ACTIVE_INDEX_KEY = "JWTS_ACTIVE_INDEX_KEY";

$(function () {
  tokenUrl = window.location.hash.substr(1).split("&")[0].split("=");
  check_token_fragment();
  token = localStorage.getItem("JWTS_LOCAL_KEY");
  localStorage.setItem("token", token);

  if (token === null || token === undefined) {
    permissions = []// ["get:movies", "get:actors"]; // default permissions
    // localStorage.setItem("permissions", permissions);
    localStorage.setItem("loggedIn", false);
    localStorage.setItem("permsLength", permissions.length);
    hideOnLogin(permissions);
  } else {
    try {
      localStorage.setItem("loggedIn", true);
      permissions = JSON.parse(atob(token.split(".")[1])).permissions;
      localStorage.setItem("permissions", permissions);
      localStorage.setItem("permsLength", permissions.length);
      if (!localStorage.getItem("permissions")) {
        permissions = ["get:movies", "get:actors"]; // default permissions
        localStorage.setItem("permissions", permissions);
      }
    } catch (e) {
      console.log("E: ", e);
    }
    hideOnLogin(permissions);
    // sendData();
  }
});
// delete movie
async function deleteMovie(movieId) {
  try {
    const data = await sendData(`/movies/${movieId}`, "", "DELETE");
    if (data.success) {
      location.reload();
      location.href = "/movies#ViewMovies";
    } else {
      throw data.message;
    }
  } catch (error) {
    iziToast.error({
      title: "Error",
      message: error,
    });
  }
}
async function postMovie() {
  title = formElem.elements["title"].value;
  Release = formElem.elements["Release"].value;
  Details = formElem.elements["Details"].value;
  dataObj = {
    title: title,
    Release: Release,
    Details: Details,
  };
  postdata = [];
  postdata.push(dataObj);
  try {
    const data = await sendData("/movies", postdata, "POST");
    if (data.success) {
      location.reload();
      location.href = "/movies#ViewMovies";
    } else {
      throw data.message;
    }
  } catch (error) {
    iziToast.error({
      title: "Error",
      message: error,
    });
  }
}
async function postActor() {
  name = formElem.elements["name"].value;
  age = formElem.elements["age"].value;
  gender = formElem.elements["gender"].value;
  dataObj = {
    actorName: name,
    age: age,
    gender: gender,
  };
  postdata = [];
  postdata.push(dataObj);

  try {
    const data = await sendData("/actors", postdata, "POST");
    if (data.success) {
      location.reload();
      location.href = "/actors#ViewActors";
    } else {
      throw data.message;
    }
  } catch (error) {
    iziToast.error({
      title: "Error",
      message: error,
    });
  }
}
async function deleteActor(actorId) {
  try {
    const data = await sendData(`/actors/${actorId}`, "", "DELETE");
    if (data.success) {      
      location.reload();
      location.href = "/actors#ViewActors";
    } else {
      throw data.message;
    }
  } catch (error) {
    iziToast.error({
      title: "Error",
      message: error,
    });
  }
}

const sendData = async (url, data, method) => {
  // Default options are marked with *
  const response = await fetch(url, {
    method,
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: new Headers({
      Authorization: `Bearer ${localStorage.getItem("JWTS_LOCAL_KEY")}`,
      "Content-Type": "application/json",
    }),
    redirect: "follow",
    referrer: "no-referrer",
    body: JSON.stringify(data),
  });

  return await response.json(); // parses JSON response into native JavaScript objects
};
myVar = localStorage.getItem("permissions");

function hideOnLogin(permissions) {
  if (permissions.length >= 2) {
    localStorage.setItem("loggedIn", true);
    document.getElementById("signin_signup").remove();
    document.getElementById("ManageCastingtitle").innerHTML = "Manage Casting";
    document.getElementById("loginBtn").remove();
  } 
  else if (permissions.length < 2){
    localStorage.setItem("loggedIn", false);
    document.getElementById("logoutBtn").remove();
    document.getElementById("viewActorz").remove();
    document.getElementById("ViewMoviez").remove();
    document.getElementById("ManageCastingtitle").innerHTML =
      "login or signup to Manage Casting";
  }
}

function check_token_fragment() {
  // parse the fragment
  const fragment = tokenUrl;
  // check if the fragment includes the access token
  if (fragment[0] === "access_token") {
    // add the access token to the jwt
    token = fragment[1];
    localStorage.setItem(JWTS_LOCAL_KEY, token);
    // save jwts to localstore
    set_jwt();
  } else if (fragment[0] === "ViewMovies") {
    token = localStorage.getItem(JWTS_LOCAL_KEY);
    set_jwt();
  }
}

function set_jwt() {
  if (token) {
    decodeJWT(token);
  }
}

function load_jwts() {
  token = localStorage.getItem(JWTS_LOCAL_KEY) || null;
  if (token) {
    decodeJWT(token);
  }
}

function activeJWT() {
  return token;
}

function decodeJWT(token) {
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
  payload = JSON.parse(jsonPayload);
  localStorage.setItem("permissions", payload.permissions);
  return payload;
}

const logOut = () => {
  token = "";
  payload = null;
  permissions = '';
  set_jwt();
  localStorage.clear();
  window.location.href = "https://fsndy.auth0.com/v2/logout";
};
