import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const SlidePanel = ({ title, content }) => {
  const panelRef = useRef(null);
  const innerRef = useRef(null);

  useEffect(() => {
    // Slide up animation
    gsap.fromTo(innerRef.current,
      { y: '100%', opacity: 0 },
      {
        y: '0%',
        opacity: 1,
        scrollTrigger: {
          trigger: panelRef.current,
          start: 'top bottom',
          end: 'top top',
          scrub: true,
        }
      }
    );

    // Mouse tilt effect
    const handleMouseMove = (e) => {
      const { left, top, width, height } = innerRef.current.getBoundingClientRect();
      const x = (e.clientX - left) / width - 0.5;
      const y = (e.clientY - top) / height - 0.5;

      gsap.to(innerRef.current, {
        rotationY: x * 20,
        rotationX: -y * 20,
        x: x * 30,
        y: y * 30,
        duration: 0.5,
        ease: 'power2.out',
      });
    };

    const handleMouseLeave = () => {
      gsap.to(innerRef.current, {
        rotationY: 0,
        rotationX: 0,
        x: 0,
        y: 0,
        duration: 0.8,
        ease: 'elastic.out(1, 0.3)',
      });
    };

    const element = innerRef.current;
    element.addEventListener('mousemove', handleMouseMove);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mousemove', handleMouseMove);
      element.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return (
    <div 
      ref={panelRef}
      style={{
        height: '100vh',
        display: 'flex',
        alignItems: 'flex-end',
        padding: '10vh 10vw',
        perspective: '1200px',
      }}
    >
      <div 
        ref={innerRef}
        style={{
          background: 'rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '24px',
          padding: '4rem',
          width: '100%',
          maxWidth: '600px',
          transformStyle: 'preserve-3d',
        }}
      >
        <h2 style={{ fontSize: '2.5rem', marginBottom: '1.5rem', color: 'var(--accent)' }}>{title}</h2>
        <p style={{ fontSize: '1.2rem', lineHeight: 1.6, color: 'var(--text-muted)' }}>{content}</p>
      </div>
    </div>
  );
};

export default SlidePanel;
