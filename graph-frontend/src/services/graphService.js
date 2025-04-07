import axios from "axios";

export const fetchGraphData = async () => {
  const response = await axios.get('http://localhost:5000/graph/data');
  console.log('API返回数据:', response.data); // 调试用
  return response.data; // 确保返回数据
};
