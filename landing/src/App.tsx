import "./App.css";
import { VscGithubInverted } from "react-icons/vsc";
import { useState } from "react";

function App() {
  const [format, setFormat] = useState<string>("png");
  const [imageUrl, setImageUrl] = useState<string>(
    "https://images.pexels.com/photos/27200179/pexels-photo-27200179/free-photo-of-landscape-of-hill-behind-flowers.jpeg",
  );
  const [resizeWidth, setResizeWidth] = useState<number | string>(200);
  const [resizeHeight, setResizeHeight] = useState<number | string>(200);
  const [quality, setQuality] = useState<string | number>();

  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string>("");

  const handleSubmit = () => {
    if (!imageUrl) {
      setError("Please fill the image url");
      return;
    } else {
      setError(null);
    }

    const options = [];
    if (format) {
      options.unshift(`format(${format})`);
    }

    if (resizeWidth && resizeHeight) {
      options.unshift(`size(${resizeWidth},${resizeHeight})`);
    }

    if (quality) {
      options.unshift(`quality(${quality})`);
    }

    setResult(
      `https://img.phake.app/${options.length > 0 ? options.join(":") : "default"}/${imageUrl}`,
    );
  };

  return (
    <div className="flex mt-24 justify-center items-center">
      <div className="container p-4 prose">
        <h1 className="text-zinc-900">Image Proxy</h1>
        <p className="text-zinc-700">A simple image converter API.</p>

        <div className="relative flex gap-4">
          <input
            type="text"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            className="w-full border px-4 py-2 rounded border-zinc-200"
            placeholder="Enter image url"
          />
        </div>

        <div className="relative mt-4 flex gap-4 whitespace-nowrap flex-wrap text-sm">
          <div className="relative flex gap-2 items-center">
            <label htmlFor="format">
              Image <b>format</b>
            </label>
            <select
              className="border border-zinc-200 px-2 py-1 rounded"
              name="format"
              id="format"
              value={format}
              onChange={(e) => {
                setFormat(e.target.value);
              }}
            >
              <option value="png">.PNG</option>
              <option value="jpeg">.JPEG</option>
              <option value="webp">.WEBP</option>
            </select>
          </div>
          <div className="relative flex gap-2 items-center">
            <label htmlFor="resizeWidth">
              and resize to <b>width</b> ={" "}
            </label>
            <input
              className="border w-24 border-zinc-200 px-2 py-1 rounded"
              name="resizeWidth"
              id="resizeWidth"
              type="number"
              value={resizeWidth}
              onChange={(e) => {
                setResizeWidth(e.target.value);
              }}
              placeholder="width"
            />
            x <b>height</b>=
            <input
              className="border w-24 border-zinc-200 px-2 py-1 rounded"
              name="resizeHeight"
              id="resizeHeight"
              value={resizeHeight}
              onChange={(e) => {
                setResizeHeight(e.target.value);
              }}
              type="number"
              placeholder="height"
            />
          </div>
          {format === "webp" && (
            <div className="relative flex gap-2 items-center">
              <label htmlFor="resizeWidth">
                and image <b>quality</b> will optimize to
              </label>
              <input
                className="border w-24 border-zinc-200 px-2 py-1 rounded"
                name="resizeWidth"
                id="resizeWidth"
                type="number"
                placeholder="75"
                value={quality}
                onChange={(e) => {
                  setQuality(e.target.value);
                }}
              />{" "}
              %
            </div>
          )}
        </div>

        <div className="mt-8">
          <button
            onClick={() => {
              handleSubmit();
            }}
            className="bg-blue-600 font-semibold w-full block text-white shrink-0 rounded px-4 py-2"
          >
            Get
          </button>
        </div>

        {!!result && (
          <>
            <div className="font-semibold mt-4">RESULT:</div>
            <textarea
              rows={5}
              className="mt-2 w-full px-4 py-2 rounded bg-blue-50 border border-blue-200 text-blue-500"
            >
              {result}
            </textarea>
          </>
        )}

        {!!error && (
          <div className="mt-4 px-4 rounded py-2 text-sm bg-red-50 border border-red-200 text-red-500">
            {error}
          </div>
        )}

        <hr />
        <p className="text-sm flex gap-1 justify-center items-center">
          <a
            className="inline-flex gap-1 items-center"
            href="https://github.com/fuongz/image-proxy"
            target="_blank"
          >
            <VscGithubInverted /> Source code
          </a>
          | Created by{" "}
          <a href="https://phuongphung.com/?ref=image-proxy" target="_blank">
            fuongz
          </a>
          .
        </p>
      </div>
    </div>
  );
}

export default App;
