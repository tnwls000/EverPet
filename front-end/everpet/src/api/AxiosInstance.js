import axios from "axios";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_LOCALHOST_URL,
});

let alertShown = false;

axiosInstance.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    const newAccessToken = response.headers["accesstoken"];
    if (newAccessToken) {
      localStorage.setItem("accessToken", newAccessToken);
    }
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const response = await axiosInstance(originalRequest);
        const newAccessToken = response.headers["accesstoken"];

        if (newAccessToken) {
          localStorage.setItem("accessToken", newAccessToken);
          axiosInstance.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${newAccessToken}`;
          originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        }

        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error("Token refresh failed", refreshError);
        localStorage.removeItem("accessToken");

        if (!alertShown) {
          alertShown = true;
          alert("로그인이 만료되었습니다. 다시 로그인해주세요.");
          window.location.href = "/";
        }
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
