// server/server.js
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors({
    origin: 'https://localhost:5173',
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true
}));
app.use(express.json()); // JSON 형식의 요청 본문을 파싱하기 위한 미들웨어 추가

app.post('/user', (req, res) => {
    const { userId, password, name, email, phoneNumber } = req.body;
    // 요청 본문에서 필요한 데이터 추출 및 처리
    res.json({ message: 'User data received!' });
});

app.post('/robot', (req, res) => {
    // 로봇 정보 처리
    const { userId, robotSerialNumber, robotName, robotStyle, robotGender } = req.body;
    res.json({ message: 'Robot data received!' });
});

app.listen(8080, () => {
    console.log('Server is running on port 8080');
});