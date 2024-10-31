document.querySelectorAll('.content-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      const rotation = Math.random() * 5 - 3;
      card.style.transform = `rotate(${rotation}deg) scale(1.1)`;
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'none';
    });

    card.addEventListener('mousedown', event => {
      if (event.button === 0) {
        card.style.transform = 'scale(0.9)';
      }
    });

    card.addEventListener('mouseup', event => {
      if (event.button === 0) {
        card.style.transform = 'none';
      }
    });
  });