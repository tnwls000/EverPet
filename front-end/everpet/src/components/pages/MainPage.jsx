//import React from 'react'
import "@/css/Font.css";

function MainPage () {
  const imageUrl = '/everpet_round_eyes.svg'
  return (
    
    <div className="home-image">
      {/* <a href="https://react.dev" target="_blank"> */}
      <img src={imageUrl} alt="Everpet Round Eyes" className="responsive-image"/>
      {/* </a> */}
      <div>
        <p> </p>
        <p> </p>
        <h2 className="Ownglyph-text">&quot; 일상을 공유하며 곁에 항상 머물러줄 나의 친구 &quot;</h2>
        <p> </p>
        <p> </p>
        <h1 className="Tmoney-text">EverPet에 오신걸 환영합니다</h1>
      </div>
    </div>
  )
}

export default MainPage
