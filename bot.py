<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Design App Mini App</title>
  
  <style>
    body {
      background-color: #0b0c0e;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #ffffff;
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    .app-container {
      max-width: 450px;
      margin: 0 auto;
      padding: 15px;
      padding-bottom: 90px; /* Отступ снизу, чтобы контент не перекрывался меню */
    }

    /* Блок с котиком и приветствием сверху */
    .welcome-block {
      display: flex;
      align-items: center;
      gap: 15px;
      background: linear-gradient(135deg, #141619, #1c1f24);
      border: 1px solid rgba(255, 0, 127, 0.2);
      border-radius: 16px;
      padding: 15px;
      margin-bottom: 25px;
    }

    /* Простой CSS Котик */
    .cat-avatar {
      position: relative;
      width: 60px;
      height: 60px;
      flex-shrink: 0;
    }
    .cat-ear-l, .cat-ear-r { position: absolute; top: -5px; width: 16px; height: 16px; background: #423127; border-radius: 50% 50% 0 0; }
    .cat-ear-l { left: 5px; transform: rotate(-15deg); }
    .cat-ear-r { right: 5px; transform: rotate(15deg); }
    .cat-head-draw { position: absolute; width: 60px; height: 50px; background: #6e5242; border-radius: 25px; bottom: 0; }
    .cat-eye-l, .cat-eye-r { position: absolute; top: 18px; width: 8px; height: 8px; background: #241c18; border-radius: 50%; }
    .cat-eye-l { left: 15px; }
    .cat-eye-r { right: 15px; }
    .cat-muzzle-draw { position: absolute; bottom: 5px; left: 17px; width: 26px; height: 14px; background: #fcfaf2; border-radius: 8px; }
    .cat-nose-draw { position: absolute; top: 2px; left: 10px; width: 6px; height: 4px; background: #ff94b8; border-radius: 50%; }

    .welcome-text h4 { margin: 0; font-size: 16px; font-weight: 700; color: #ffffff; }
    .welcome-text p { margin: 4px 0 0 0; font-size: 13px; color: #ff66cc; }

    /* Заголовки страниц */
    .section-title {
      font-size: 20px;
      font-weight: 800;
      margin: 0 0 15px 0;
      color: #ffffff;
    }

    /* Список тарифов */
    .tariffs-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 20px;
    }
    .tariff-card {
      background: #141619;
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 14px;
      padding: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .tariff-card.selected {
      border-color: #ff007f;
      background: rgba(255, 0, 127, 0.05);
      box-shadow: 0 0 15px rgba(255, 0, 127, 0.1);
    }
    .tariff-info { display: flex; flex-direction: column; gap: 4px; text-align: left; max-width: 70%; }
    .tariff-name { font-size: 15px; font-weight: 700; color: #ffffff; }
    .tariff-desc { font-size: 12px; color: #94a3b8; line-height: 1.3; }
    .tariff-price { text-align: right; font-size: 16px; font-weight: 800; color: #ff66cc; }

    /* Поля ввода формы */
    .form-group {
      margin-bottom: 15px;
      text-align: left;
    }
    .form-group label {
      display: block;
      font-size: 13px;
      color: #94a3b8;
      margin-bottom: 6px;
    }
    .form-control {
      width: 100%;
      background: #141619;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 12px;
      color: #ffffff;
      font-size: 14px;
      box-sizing: border-box;
      outline: none;
    }
    .form-control:focus {
      border-color: #ff66cc;
    }

    /* Кнопка отправки */
    .submit-btn {
      width: 100%;
      background: linear-gradient(135deg, #ff007f, #ff66cc);
      color: #ffffff;
      border: none;
      border-radius: 12px;
      padding: 15px;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      box-sizing: border-box;
      margin-top: 10px;
    }
    .submit-btn:active {
      transform: scale(0.98);
    }

    /* Навигация (вкладки) */
    .tab-content { display: none; }
    .tab-content.active { display: block; }

    .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 100%;
      max-width: 450px;
      background: #0d0e10;
      display: flex;
      justify-content: space-around;
      padding: 12px 0;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      z-index: 1000;
    }
    .nav-item {
      background: none;
      border: none;
      color: #64748b;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      flex: 1;
      text-align: center;
    }
    .nav-item.active { color: #ff66cc; }

    /* Страница информации */
    .info-card {
      background: #141619;
      border-radius: 14px;
      padding: 15px;
      text-align: left;
      margin-bottom: 15px;
    }
    .info-card h4 { margin: 0 0 8px 0; color: #ff66cc; }
    .info-card p { margin: 0; font-size: 13px; color: #94a3b8; line-height: 1.4; }
    .manager-link {
      display: inline-block;
      margin-top: 10px;
      color: #ffffff;
      background: #242830;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 13px;
      text-decoration: none;
    }
  </style>

  <!-- Подключаем Telegram SDK -->
  <script src="https://telegram.org/js/telegram-web-app.js" defer></script>
</head>
<body>

  <div class="app-container">
    
    <!-- Вкладка 1: Заказ -->
    <div id="order-tab" class="tab-content active">
      
      <!-- Шапка с котиком -->
      <div class="welcome-block">
        <div class="cat-avatar">
          <div class="cat-ear-l"></div>
          <div class="cat-ear-r"></div>
          <div class="cat-head-draw">
            <div class="cat-eye-l"></div>
            <div class="cat-eye-r"></div>
            <div class="cat-muzzle-draw"><div class="cat-nose-draw"></div></div>
          </div>
        </div>
        <div class="welcome-text">
          <h4 id="welcome-title">Привет! 👋</h4>
          <p>Давай создадим крутой дизайн</p>
        </div>
      </div>

      <h3 class="section-title">Выбери тариф</h3>
      
      <div class="tariffs-list">
        <div class="tariff-card selected" onclick="selectTariff('🌱 Бюджетный', this)">
          <div class="tariff-info">
            <span class="tariff-name">🌱 Бюджетный</span>
            <span class="tariff-desc">Стильно, быстро и без лишних переплат.</span>
          </div>
          <div class="tariff-price">590₽</div>
        </div>

        <div class="tariff-card" onclick="selectTariff('⚡ Средний', this)">
          <div class="tariff-info">
            <span class="tariff-name">⚡ Средний</span>
            <span class="tariff-desc">Идеальный баланс проработки деталей и цены.</span>
          </div>
          <div class="tariff-price">1090₽</div>
        </div>
      </div>

      <div class="form-group">
        <label>Желаемые сроки</label>
        <input type="text" id="deadline" class="form-control" placeholder="Например: 2-3 дня">
      </div>

      <div class="form-group">
        <label>Что нужно сделать? (ТЗ)</label>
        <textarea id="task" class="form-control" rows="4" placeholder="Опиши свою задачу подробно..."></textarea>
      </div>

      <button class="submit-btn" onclick="sendOrderData()">Отправить заказ</button>
    </div>

    <!-- Вкладка 2: Информация -->
    <div id="info-tab" class="tab-content">
      <h3 class="section-title">Информация</h3>
      
      <div class="info-card">
        <h4>Отзывы</h4>
        <p>⭐ <b>Александр:</b> Отличное оформление для канала, просмотры выросли!</p>
        <p style="margin-top: 8px;">⭐ <b>Кристина:</b> Карточки для маркетплейса просто супер.</p>
      </div>

      <div class="info-card">
        <h4>Сотрудничество</h4>
        <p>По вопросам крупных заказов или работы пишите напрямую менеджеру:</p>
        <a href="https://t.me/MartOkkks" class="manager-link" target="_blank">🚀 Написать менеджеру</a>
      </div>
    </div>

  </div>

  <!-- Нижнее меню навигации -->
  <nav class="bottom-nav">
    <button class="nav-item active" id="nav-order" onclick="switchTab('order-tab', this)">Заказ</button>
    <button class="nav-item" id="nav-info" onclick="switchTab('info-tab', this)">Инфо</button>
  </nav>

  <script>
    // Безопасное чтение имени пользователя из Telegram
    document.addEventListener("DOMContentLoaded", function() {
      setTimeout(() => {
        if (window.Telegram && window.Telegram.WebApp) {
          const tg = window.Telegram.WebApp;
          try {
            tg.expand();
            const user = tg.initDataUnsafe?.user;
            if (user && user.first_name) {
              document.getElementById('welcome-title').innerText = `Привет, ${user.first_name}! 👋`;
            }
          } catch (e) { console.error(e); }
        }
      }, 150);
    });

    let selectedTariffValue = "🌱 Бюджетный";

    function selectTariff(tariffName, cardElement) {
      document.querySelectorAll('.tariff-card').forEach(card => card.classList.remove('selected'));
      cardElement.classList.add('selected');
      selectedTariffValue = tariffName;
    }

    function switchTab(tabId, button) {
      document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      button.classList.add('active');
    }

    function sendOrderData() {
      const deadline = document.getElementById('deadline').value.trim();
      const task = document.getElementById('task').value.trim();
      
      if (!deadline || !task) {
        alert("Пожалуйста, заполните все поля!");
        return;
      }
      
      if (window.Telegram && window.Telegram.WebApp) {
        const tg = window.Telegram.WebApp;
        const data = {
          tariff: selectedTariffValue,
          deadline: deadline,
          task: task
        };
        tg.sendData(JSON.stringify(data));
        tg.close();
      } else {
        alert("Данные сохранены (работает только внутри Telegram)");
      }
    }
  </script>
</body>
</html>
