import { useCurrentFrame, interpolate } from "remotion";

export const MyComposition = () => {
  const fps = 30;
  const durationInSeconds = 5;
  const totalFrames = fps * durationInSeconds;
  const currentFrame = useCurrentFrame();

  // Interpolate the percentage from 0 to 95 over the video duration
  const percentage = interpolate(currentFrame, [0, totalFrames], [0, 95]);

  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      height: "100%",
      backgroundColor: "#f0f0f0"
    }}>
      {/* Bar container */}
      <div style={{
        width: "400px",
        height: "40px",
        backgroundColor: "#e0e0e0",
        borderRadius: "20px",
        overflow: "hidden",
        marginRight: "20px"
      }}>
        {/* Animated bar */}
        <div style={{
          width: `${percentage}%`,
          height: "100%",
          backgroundColor: "#4287f5",
          transition: "width 0.1s linear"
        }}></div>
      </div>

      {/* Percentage text */}
      <div style={{
        fontSize: "36px",
        fontWeight: "bold",
        color: "#333"
      }}>
        {Math.round(percentage)}%
      </div>
    </div>
  );
};
