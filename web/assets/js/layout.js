(function(){
  const header = document.getElementById('site-header');
  const footer = document.getElementById('site-footer');

  if(header){
    header.innerHTML = `
      <nav class="nav" aria-label="主导航">
        <div class="container nav__bar">
          <a class="nav__logo" href="index.html">长沙望眼科技有限公司</a>
          <div class="nav__menu" role="menubar">
            <a role="menuitem" href="about.html">关于我们</a>
            <a role="menuitem" href="services.html">服务</a>
            <a role="menuitem" href="cases.html">案例</a>
            <a role="menuitem" href="news.html">新闻</a>
            <a role="menuitem" href="videos.html">视频</a>
            <a role="menuitem" href="careers.html">加入我们</a>
            <a role="menuitem" href="contact.html">联系我们</a>
            <a class="btn btn--primary nav__cta" href="contact.html">获取方案</a>
          </div>
        </div>
      </nav>
    `;
  }

  if(footer){
    footer.innerHTML = `
      <div class="footer">
        <div class="container footer__grid">
          <section>
            <h4>长沙望眼科技有限公司</h4>
            <p>专注行车记录与道路安全，提供车载影像与安全应用解决方案。</p>
            <div class="social" aria-label="社交媒体">
              <a href="https://www.douyin.com/" target="_blank" aria-label="抖音（TikTok）" rel="noreferrer noopener">
                <img class="icon" alt="抖音" src="https://cdn.simpleicons.org/tiktok/ffffff" />
              </a>
              <a href="https://weibo.com/" target="_blank" aria-label="微博" rel="noreferrer noopener">
                <img class="icon" alt="微博" src="https://cdn.simpleicons.org/sinaweibo/ffffff" />
              </a>
              <a href="https://space.bilibili.com/" target="_blank" aria-label="哔哩哔哩" rel="noreferrer noopener">
                <img class="icon" alt="哔哩哔哩" src="https://cdn.simpleicons.org/bilibili/ffffff" />
              </a>
              <a href="https://www.xiaohongshu.com/" target="_blank" aria-label="小红书" rel="noreferrer noopener">
                <img class="icon" alt="小红书" src="https://cdn.simpleicons.org/xiaohongshu/ffffff" onerror="this.onerror=null;this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\'%3E%3Crect width=\'24\' height=\'24\' rx=\'4\' fill=\'%23ff2442\'/%3E%3Cpath d=\'M7 7h10v10H7z\' fill=\'%23fff\'/%3E%3C/svg%3E'" />
              </a>
            </div>
          </section>
          <section>
            <h4>公司</h4>
            <ul>
              <li><a href="about.html">关于我们</a></li>
              <li><a href="videos.html">视频</a></li>
              <li><a href="careers.html">加入我们</a></li>
              <li><a href="news.html">新闻</a></li>
            </ul>
          </section>
          <section>
            <h4>服务</h4>
            <ul>
              <li><a href="services.html">解决方案</a></li>
              <li><a href="cases.html">客户案例</a></li>
            </ul>
          </section>
          <section>
            <h4>联系</h4>
            <ul>
              <li><a href="contact.html">联系我们</a></li>
              <li><a href="#">隐私政策</a></li>
              <li><a href="#">条款</a></li>
            </ul>
          </section>
        </div>
        <div class="container copyright">© <span id="year"></span> Company. 保留所有权利。</div>
      </div>
    `;
    const yearEl = document.getElementById('year');
    if(yearEl){ yearEl.textContent = String(new Date().getFullYear()); }
  }
})();


