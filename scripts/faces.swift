import Vision
import AppKit
let dir = CommandLine.arguments[1]
let files = try! FileManager.default.contentsOfDirectory(atPath: dir).filter{$0.hasSuffix(".png")}.sorted()
for f in files {
  let url = URL(fileURLWithPath: dir + "/" + f)
  let req = VNDetectFaceRectanglesRequest()
  let h = VNImageRequestHandler(url: url)
  try? h.perform([req])
  if let r = (req.results ?? []).max(by: {$0.boundingBox.width < $1.boundingBox.width}) {
    let b = r.boundingBox
    print(f, String(format: "cx=%.4f cy=%.4f w=%.4f h=%.4f", b.midX, 1 - b.midY, b.width, b.height))
  } else { print(f, "none") }
}
