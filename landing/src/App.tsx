import "./App.css";

function App() {
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="container prose prose-2xl">
        <h1 className="text-zinc-900">Image Proxy</h1>
        <p className="text-zinc-700">A simple image converter API.</p>

        <pre>
          <code>
            <span className="text-green-500 font-bold">GET:</span>{" "}
            https://api.phake.app/image/format(
            <span className="text-red-500 italic">IMAGE_TYPE</span>
            ):size(<span className="text-yellow-500 italic">WIDTH</span>,
            <span className="text-yellow-500 italic">HEIGHT</span>)/
            <span className="text-blue-500 italic">IMAGE_URL</span>
          </code>
        </pre>

        <ul className="text-base">
          <li>
            <span className="font-semibold">IMAGE_TYPE</span>: can be{" "}
            <span className="font-semibold">png</span>
          </li>
          <li>
            <span className="font-semibold">WIDTH,HEIGHT</span>: resize image to
            be <code>WIDHT,HEIGHT</code> of width per size.
          </li>
          <li>
            <span className="font-semibold">IMAGE_URL</span>: is the image URI.
            URI should be encoded by <code>encodeURIComponent</code>
          </li>
        </ul>

        <hr />
        <p className="text-sm">
          Created by{" "}
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
