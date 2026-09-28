const form =
    document.getElementById("task-form");

const task =
    document.getElementById("task");

const input =
    document.getElementById("input-text");

const result =
    document.getElementById("result");

const statusElement =
    document.getElementById("status");

const submitButton =
    document.getElementById("submit-btn");

const buttonText =
    document.getElementById("button-text");

const spinner =
    document.getElementById("spinner");

const clearButton =
    document.getElementById("clear-btn");


/* --------------------------------
   PLACEHOLDERS
-------------------------------- */

const placeholders = {

    qa:
        "Example: What is the largest ocean?",

    explain:
        "Example: Explain the Pythagoras theorem in simple words.",

    quiz:
        "Paste a topic or educational passage to generate a quiz.",

    summarize:
        "Paste the educational passage you want to summarize.",

    learn:
        "Example: SQL"
};


task.addEventListener(
    "change",
    function () {

        input.placeholder =
            placeholders[task.value];

    }
);


/* --------------------------------
   STATUS
-------------------------------- */

function setStatus(
    message,
    error = false
) {

    statusElement.textContent =
        message;

    statusElement.classList.toggle(
        "error",
        error
    );
}


/* --------------------------------
   LOADING
-------------------------------- */

function setLoading(
    loading
) {

    submitButton.disabled =
        loading;

    spinner.classList.toggle(
        "hidden",
        !loading
    );

    buttonText.textContent =
        loading
            ? "Working..."
            : "Generate";
}


/* --------------------------------
   HTML ESCAPE
-------------------------------- */

function escapeHtml(
    value
) {

    return String(value)
        .replaceAll(
            "&",
            "&amp;"
        )
        .replaceAll(
            "<",
            "&lt;"
        )
        .replaceAll(
            ">",
            "&gt;"
        )
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );
}


/* --------------------------------
   RENDER RESULT
-------------------------------- */

function renderResult(
    type,
    data
) {


    /* Q&A */

    if (type === "qa") {

        result.innerHTML = `
            <div class="answer">
                ${escapeHtml(data.answer)}
            </div>
        `;

        return;
    }


    /* EXPLANATION */

    if (type === "explain") {

        result.innerHTML = `
            <div class="answer">
                ${escapeHtml(
                    data.explanation
                )}
            </div>

            <p class="muted">
                Engine:
                ${escapeHtml(
                    data.engine
                )}
            </p>
        `;

        return;
    }


    /* SUMMARY */

    if (type === "summarize") {

        result.innerHTML = `
            <div class="answer">
                ${escapeHtml(
                    data.summary
                )}
            </div>
        `;

        return;
    }


    /* QUIZ */

    if (type === "quiz") {

        result.innerHTML =
            data.questions
                .map(
                    (
                        question,
                        index
                    ) => {

                        return `
                            <article
                                class="quiz-question"
                            >

                                <h3>
                                    ${index + 1}.
                                    ${escapeHtml(
                                        question.question
                                    )}
                                </h3>

                                ${question.options
                                    .map(
                                        option => `
                                            <div
                                                class="quiz-option"
                                            >
                                                ${escapeHtml(
                                                    option
                                                )}
                                            </div>
                                        `
                                    )
                                    .join("")
                                }

                                <p class="correct">

                                    <strong>
                                        Correct Answer:
                                    </strong>

                                    ${escapeHtml(
                                        question.correct_answer
                                    )}

                                </p>

                                <p>
                                    ${escapeHtml(
                                        question.explanation
                                    )}
                                </p>

                            </article>
                        `;
                    }
                )
                .join("");

        return;
    }


    /* LEARNING PATH */

    if (type === "learn") {

        result.innerHTML = `

            <h3>
                ${escapeHtml(
                    data.topic
                )}
            </h3>


            ${data.learning_path
                .map(
                    (
                        step,
                        index
                    ) => {

                        return `
                            <article
                                class="learning-step"
                            >

                                <h3>
                                    ${index + 1}.
                                    ${escapeHtml(
                                        step.level
                                    )}
                                </h3>

                                <p>

                                    <strong>
                                        Timeline:
                                    </strong>

                                    ${escapeHtml(
                                        step.timeline
                                    )}

                                </p>

                                <p>

                                    <strong>
                                        Topics:
                                    </strong>

                                    ${step.topics
                                        .map(
                                            escapeHtml
                                        )
                                        .join(
                                            ", "
                                        )}

                                </p>

                                <p>

                                    <strong>
                                        Resources:
                                    </strong>

                                    ${step.resources
                                        .map(
                                            escapeHtml
                                        )
                                        .join(
                                            ", "
                                        )}

                                </p>

                            </article>
                        `;
                    }
                )
                .join("")
            }


            <h3>
                Study Tips
            </h3>


            <ul>

                ${data.tips
                    .map(
                        tip => `
                            <li>
                                ${escapeHtml(
                                    tip
                                )}
                            </li>
                        `
                    )
                    .join("")
                }

            </ul>
        `;

    }

}


/* --------------------------------
   CLEAR
-------------------------------- */

clearButton.addEventListener(
    "click",
    function () {

        input.value = "";

        result.innerHTML = `
            <p class="muted">
                Your AI-generated result
                will appear here.
            </p>
        `;

        setStatus("Ready");

    }
);


/* --------------------------------
   FORM SUBMISSION
-------------------------------- */

form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const text =
            input.value.trim();


        if (!text) {

            setStatus(
                "Please enter some text.",
                true
            );

            return;
        }


        const endpoints = {

            qa:
                "/qa",

            explain:
                "/explain",

            quiz:
                "/quiz",

            summarize:
                "/summarize",

            learn:
                "/learn/recommendations"
        };


        const type =
            task.value;


        setLoading(true);

        setStatus(
            "Generating..."
        );


        try {

            const response =
                await fetch(
                    endpoints[type],
                    {

                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                text: text
                            })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Server error."
                );
            }


            renderResult(
                type,
                data
            );


            setStatus(
                "Complete"
            );


        } catch (error) {

            result.innerHTML = `

                <p class="answer">

                    ${escapeHtml(
                        error.message
                    )}

                </p>

                <p class="muted">

                    Check that the FastAPI
                    server is running and
                    your GEMINI_API_KEY
                    is configured.

                </p>
            `;


            setStatus(
                "Error",
                true
            );


        } finally {

            setLoading(false);

        }

    }
);