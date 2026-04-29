import React from 'react';
import SlidePanel from './SlidePanel';

const ContentStack = () => {
  const sections = [
    {
      title: "Section One",
      content: "This is a generic section to demonstrate the sliding panel effect. The panel slides up from the bottom and tilts according to your mouse position."
    },
    {
      title: "Section Two",
      content: "Everything in this template is designed to be fully modular and easy to rip apart. Use it as a base for your cinematic projects."
    },
    {
      title: "Section Three",
      content: "Final generic section. Scroll down more to see the end of the journey. The background video continues to scrub as you move through these panels."
    }
  ];

  return (
    <div className="content-stack">
      {sections.map((section, i) => (
        <SlidePanel key={i} title={section.title} content={section.content} />
      ))}
    </div>
  );
};

export default ContentStack;
