import Vision
import AppKit
// shift <dir>: frame-to-frame translation (px of the analysed frame) between consecutive PNGs
let dir = CommandLine.arguments[1]
let files = try! FileManager.default.contentsOfDirectory(atPath: dir).filter{$0.hasSuffix(".png")}.sorted()
func cg(_ f: String) -> CGImage { let i = NSImage(contentsOfFile: dir + "/" + f)!; var r = CGRect(origin: .zero, size: i.size); return i.cgImage(forProposedRect: &r, context: nil, hints: nil)! }
var prev = cg(files[0]); print("0 0 0")
for (k, f) in files.dropFirst().enumerated() {
  let cur = cg(f)
  let req = VNTranslationalImageRegistrationRequest(targetedCGImage: cur)
  try? VNImageRequestHandler(cgImage: prev).perform([req])
  let t = (req.results?.first as? VNImageTranslationAlignmentObservation)?.alignmentTransform ?? .identity
  print(k + 1, String(format: "%.2f %.2f", t.tx, t.ty)); prev = cur
}
