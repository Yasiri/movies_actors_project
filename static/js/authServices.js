var token = "";
var payload = "";
var tokenUrl = "";
let permissions;
const JWTS_LOCAL_KEY = "JWTS_LOCAL_KEY";
const JWTS_ACTIVE_INDEX_KEY = "JWTS_ACTIVE_INDEX_KEY";

$(function () {
  // get token from URL 
  tokenUrl = window.location.hash.substr(1).split("&")[0].split("=");

  check_token_fragment();

  // get token from {JWTS_LOCAL_KEY} constant after checking fragment
  token = localStorage.getItem("JWTS_LOCAL_KEY");
  // save token to local storage
  localStorage.setItem("token", token);

  // check token has permissons if not 
  // set permissons to null and login status to false
  if (token === null || token === undefined) {
    permissions = [];
    localStorage.setItem("loggedIn", false);
    localStorage.setItem("permsLength", permissions.length);
    hideOnLogin(permissions);
  } else {
      try {
        // set default permissions ["get:movies", "get:actors"]
        localStorage.setItem("loggedIn", true);
        permissions = JSON.parse(atob(token.split(".")[1])).permissions;
        localStorage.setItem("permissions", permissions);
        localStorage.setItem("permsLength", permissions.length);

        if (!localStorage.getItem("permissions")) {
          permissions = ["get:movies", "get:actors"];
          localStorage.setItem("permissions", permissions);
        }
      } catch (e) {
        console.log("Error: ", e);
      }
    // based on the permissons found 
    // hide or show login or signup 
    // also hides other features 
    hideOnLogin(permissions);
  }
});

/*
 postMovie sends request to /movies endpint  
 with method {POST} to create a new movie 

*/
async function postMovie() {
  title = formElem.elements["title"].value;
  Release = formElem.elements["Release"].value;
  Details = formElem.elements["Details"].value;

  // construct a movie object 
  dataObj = {
    title: title,
    release_date: Release,
    movie_details: Details,
  };
  // holds list of movie object 
  postdata = [];
  // appened movie object to postdata array
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
    message = '';
    if(error == undefined){
      iziToast.error({
        title: "Error",
        message: 'Movie ALready Exists..',
      });
    }
    else {
      iziToast.error({
        title: "Error",
        message: error,
      });
    }
  }
}

/**
 deleteMovie sends request to /movies/${movieId} endpint 
 with method {DELETE} to delete a movie 

 @param {*} movieId the id of the movie to be deleted
*/
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

/*
 postActor sends request to /actors endpint  
 with method {POST} to create a new actor 

*/
async function postActor() {
  name = formElem.elements["name"].value;
  age = formElem.elements["age"].value;
  gender = formElem.elements["gender"].value;

  // construct a actor object 
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

/** 
 deleteActor sends request to/actors/${actorId} endpint 
 with method {DELETE} to delete an actor 

 @param {*} actorId the id of the actor to be deleted
*/
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

/*
 sendAssignData construct headers with needed payload
 and response for assigning actors to movies endpoint 
*/
const sendAssignData = async (url, data, method) => {
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
    });
    return await response.json();
};
const sendData = async (url, data, method) => {
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

  return await response.json();
};

/**
 * hideOnLogin function is used to show and hide
 * elements in the frontend for each user based
 * on their permissions also if logged in or not
 * 
 * @param {*} permissions permissons found for the user
 */
function hideOnLogin(permissions) {
  if (permissions.length >= 2) {
    localStorage.setItem("loggedIn", true);
    document.getElementById("signin_signup").remove();
    document.getElementById("ManageCastingtitle").innerHTML = "Manage Casting";
    document.getElementById("loginBtn").remove();
  } else if (permissions.length < 2) {
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

/**
 * logOut users from the app and reset all 
 * variables for next login
 */
const logOut = () => {
  token = "";
  payload = null;
  permissions = "";
  set_jwt();
  localStorage.clear();
  window.location.href = "https://fsndy.auth0.com/v2/logout";
};
