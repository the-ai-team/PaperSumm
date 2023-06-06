import styles from '@/styles/Animation.module.css';
import { useEffect, useState } from 'react';

export function AnimationBackground() {
  const circleRadius = 200;
  const increment = 4;
  const hideStartFrom = 10;
  const interval = 10;
  const maxVisible = 100;
  const [xDirection, setXDirection] = useState(1);
  const [yDirection, setYDirection] = useState(1);
  const [circles, setCircles] = useState([]);

  useEffect(() => {
    const paintCircles = () => {
      const lastCircle = circles[circles.length - 1] || {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        a: 1,
      };

      if (lastCircle.y > window.innerHeight - circleRadius * 2) {
        setYDirection(-1);
      }
      if (lastCircle.y < 0) {
        setYDirection(1);
      }
      if (lastCircle.x > window.innerWidth - circleRadius * 2) {
        setXDirection(-1);
      }
      if (lastCircle.x < 0) {
        setXDirection(1);
      }

      const x = lastCircle.x + increment * xDirection;
      const y = lastCircle.y + increment * yDirection;
      const a = 1;

      // Decreasing opacity
      const newCircles = [...circles.slice(-maxVisible + 1), { x, y, a }];
      for (let i = 0; i < circles.length; i++) {
        if (i > circles.length - hideStartFrom - 1) {
          continue;
        }
        newCircles[i].a -= 1 / (circles.length - hideStartFrom);
      }

      setCircles(newCircles);
    };

    setTimeout(paintCircles, interval);

    return () => {
      clearTimeout(paintCircles);
    };
  }, [circles, xDirection, yDirection]);

  return (
    <div>
      {circles.map((circle, index) => {
        return (
          <div
            className={styles.circle}
            key={index}
            style={{
              left: circle.x,
              top: circle.y,
              width: circleRadius * 2,
              opacity: circle.a,
            }}
          ></div>
        );
      })}
    </div>
  );
}
