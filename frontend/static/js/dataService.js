const postData = async (url, data, method) => {
  const response = await fetch(url, {
    method,
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: new Headers({
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    }),
    redirect: "follow",
    referrer: "no-referrer",
    body: data,
  });
  return await response.json();
};

 async () => {
  try {
    const data = await postData("/", response, "POST");
    if (data.success) {
      location.href = "/";
    } else {
      throw data.message;
    }
  } catch (error) {
    iziToast.error({
      title: "Error",
      message: error,
    });
  }
};
