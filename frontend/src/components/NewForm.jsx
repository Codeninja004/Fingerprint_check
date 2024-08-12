import { useRef, useState } from "react";
import axios from "axios";
import { MdFingerprint } from "react-icons/md";
import { VscLoading } from "react-icons/vsc";
import { TbCheckbox } from "react-icons/tb";
import { BiErrorCircle } from "react-icons/bi";

function NewForm() {
  const [submit, setSubmit] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [score, setScore] = useState("");
  const [uploaded, setUploaded] = useState(false);

  const inputFileRef = useRef();

  function uploadhandler() {
    inputFileRef.current.click();
    setIsError(false);
    setIsLoading(false);
  }

  function imageInputHandler() {
    setSubmit(true);
  }

  async function uploadFile(newData) {
    setIsLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/media/upload/new",
        newData
      );
      if (response) {
        setIsLoading(false);
      }
      if (!response.data.score) {
        setIsError(true);
        setSubmit(false);
        setScore(response.data);
        return;
      }
      setScore(response.data);
      setUploaded(true);
    } catch (e) {
      setIsLoading(false);
      setSubmit(false);
      setIsError(true);
    }
  }

  const submitHandler = async (event) => {
    event.preventDefault();
    const file = inputFileRef.current.files[0];
    let data = new FormData();
    data.append("file", file);
    uploadFile(data);
  };

  return (
    <form className=" bg-white flex flex-col justify-between items-center  border-dotted border-blue-900 border rounded-lg p-8">
      <label htmlFor="file" className=" capitalize font-bold">
        Add New Fringer Print
      </label>
      <div className=" my-4">
        <div className=" bg-black h-40 w-60 rounded-lg flex items-center justify-center flex-col">
          {!submit && !isError && (
            <MdFingerprint size={90} color="rgb(0, 255, 255)" />
          )}
          {submit && !isLoading && (
            <TbCheckbox size={90} color="rgb(0, 255, 255)" />
          )}
          {isError && <BiErrorCircle size={90} color="rgb(0, 255, 255)" />}
          <div className=" animate-spin">
            {isLoading && <VscLoading size={90} color="rgb(0, 255, 255)" />}
          </div>
          <div className="flex flex-col items-center">
            <p className=" text-teal-300 font-medium capitalize">
              {score.message} <span>{score.score}</span>
            </p>
          </div>
        </div>
        <div>
          <input
            type="file"
            id="file"
            name="file"
            required
            ref={inputFileRef}
            className=" hidden"
            onChange={imageInputHandler}
            accept="image/png, image/gif, image/jpeg, image/bmp"
          />
        </div>
      </div>
      <div>
        {!isError && !uploaded && (
          <button
            className=" bg-blue-500 rounded-md p-2 font-medium capitalize"
            type="button"
            onClick={!submit ? uploadhandler : submitHandler}
          >
            {!submit ? "upload" : isLoading ? "Loading..." : "submit"}
          </button>
        )}
        {isError && (
          <button
            className=" bg-blue-500 rounded-md p-2 font-medium capitalize cursor-pointer"
            type="button"
            onClick={() => {
              window.location.reload(false);
            }}
          >
            Try Again
          </button>
        )}
        {uploaded && (
          <button
            className=" bg-blue-500 rounded-md p-2 font-medium capitalize cursor-pointer"
            type="button"
            onClick={() => {
              window.location.reload(false);
            }}
          >
            Try Again
          </button>
        )}
      </div>
    </form>
  );
}

export default NewForm;
