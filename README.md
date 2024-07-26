Human Robot Communication

**Background**
Patients who are confined to their beds often need to shift and adjust their positions. This is
essential to accommodate various activities, including changing bed linens, having meals,
reading, sleeping, and more. Additionally, it is crucial to change the patient's position in bed
every two hours to maintain proper blood circulation, promote skin health, and prevent the
occurrence of bedsores [1]. To address this challenge, our team developed BRO (Bed Remote
Operator), a robot capable of assisting with adjusting the hospital bed's configuration based on
oral commands.

**Design**
Persona & Identity
BRO is designed with the primary function of moving patients' beds, constituting its core activity.
Although additional functionalities such as providing bedside assistance, having a conversation
with the patient are yet to be designed, it was imperative to establish a non-threatening and
friendly identity for the robot. The robot's positioning, adjacent to the patient's bed on a table,
was an important decision to improve accessibility for the patients. Careful consideration was
given to the robot's appearance to ensure visibility and clear sound transmission.
At the project's inception, the team deliberated on whether to give the robot a human voice,
considering that many real-world voice-based assistants typically have a feminine voice. We
delved into the decision, recognizing that the human ear and brain are sensitive to pitch and
timbre differences that convey information about the speaker's sex. In instances where robots
communicate through sound, these acoustic qualities significantly influence users' attributions of
sex or gender to the robot.
Recent findings highlight differing perceptions of robots between males and females, influencing
how robots are conceptualized and how humans respond to their interactions [2] (Nass, Clifford
& Moon et. al). Addressing stereotypes, biases, and gender norms was crucial in defining BRO's
identity, aiming to avoid perpetuating undesirable perceptions. Opting for a non-binary identity
was preferred to break away from traditional norms. Eventually we ended up with high-pitched
sounds without making them feminine to improve clear communication in noisy environments.

Appearance
The appearance of a robot significantly impacts its interaction with humans. For example,
anthropomorphic robots, which imitate human body structure, have been found to be more
engaging and likable in a remote setting when they mimic human body postures and expressive
gestures. [3] (Jesse Fox et. al.) However, robots that closely, but imperfectly, resemble humans
may elicit negative social and emotional responses, leading to decreased trust, a phenomenon
known as the "Uncanny Valley".
In our initial iteration, our goal was to craft a humanoid-looking robot to facilitate user interaction,
emphasizing facial features and expressions as that would improve the sociability factor of the
robot. However, we recognized the redundancy of such a representation for a robot tasked with
bed repositioning. The humanoid design failed to effectively convey the bed's functionality to
users.
This realization prompted a shift in the robot's appearance, opting for a bed-like design. This
decision aimed to offer users an intuitively relevant representation of the robot's purpose and
context based on [4] (Goetz, Jennifer & Kiesler et. al.). Simultaneously, we refined the robot's
functionality to focus solely on essential features. Prioritizing specialization in bed repositioning
over a comprehensive bedside assistant, our design became tailored specifically to its core
task.

Interaction Modalities
Once we settled on this approach, we aimed to establish a seamless means of exchanging
information with the patient. Achieving this involved selecting the most appropriate
communication modalities. Since verbal communication was prohibited by project requirements,
we opted for visual and auditory cues to convey information to the users, as recommended in [5]
(Jacqueline Urakami et. al.). These emphasized channels were chosen to relay nonverbal
signals effectively.

Audio
BRO's sound design included different types of expressions—Semantic-Free Utterances
(SFUs). These SFUs have two categories: Para-linguistic utterances and Non-linguistic
utterances, each serving specific communication purposes for the robot. [6] (Yilmazyildiz et al.)
Para-linguistic utterances (PLUs) are human-created sounds like 'ohh,' yeah,' 'hmm,' etc., which
are then synthesized using specialized audio processing software. They're used to convey
emotions subtly, adding depth to how the robot communicates. When designing these
utterances, we paid close attention to the pitch, making sure it matches the robot's physical
movements. For example, if the robot moves up, the sound goes up too, creating a coordinated
audio-visual experience. This synchronization between auditory cues and physical movements
not only improved the overall user experience but also added to the perception of the robot's
responsiveness and intelligence.
Investigation into a hospital robot's use of musical utterances revealed that individuals exposed
to musical utterances demonstrated increased cognitive empathy compared to those in a silent
condition [7] (Höfker, T.). This indicates that incorporating sound, including musical elements,
enhances empathy towards the robot, such as BRO. Simple sounds, like beeping, positively
impacted people's comprehension of the robot, instilling confidence in their interpretation. In
addition to the social aspect, sounds of the robot were also used to emphasize the significance
of tasks underway, completion and underscore the successful execution of actions. This design
approach is rooted based on the theory presented in [6] (Yilmazyildiz et al.)

Motion
In the initialization phase, both the headrest and footrest flap simultaneously, creating a
synchronized visual and auditory cue to signal the robot's readiness for user input. Conversely,
when BRO detects the 'move the bed' intent without a specified location, it initiates a sequence
of movements. The headrest flaps with a blue light, followed by the footrest's corresponding
flapping motion with its respective light. In this context, the sequence functions not only as a
signal but also as a purposeful physical response, strategically designed to prompt further
action. This was intended to convey the question ’which part of the bed shall I move?’
non-verbally. When it’s clear which part of the bed and if the direction is up or down, BRO first
moves that part of itself in the correct direction. Then it waits for confirmation, before moving the
patients’ bed.

Light
Research indicates that light signals effectively communicate a robot's intent. Platforms like
ModLight have been designed to convey a robot's movement, speed, and brightness through
light. [8] (K. Baraka et al.). Utilizing expressive lights on robots has been shown to enhance
social engagement and facilitate user comprehension of the robot's state and actions. The
application of color theory enables the design of colored light animations that convey
information about the robot's internal state. [9] (E. Saad et. al.). The light cues in BRO's design
prioritized consistency in similar contexts by utilizing uniform blue lights for actions like selecting
the headrest or footrest. This intentional color choice improved user recognition and
comprehension of the robot's responses. Additionally, the incorporation of universally
recognized colors, such as green indicating permission or 'pass,' contributed to transparent
communication. Double green lights symbolized the successful task completion, aligning with
established norms.

In instances where actions related to specific bed parts, individual lights were activated to guide
the user's focus to that specific area. For instance, manipulating only the headrest triggered the
corresponding light in that section, ensuring informative and visually directed signals, ultimately
enhancing the overall user experience.

Multi-Modality and Interdependence
To illustrate how the different modalities worked together cohesively, let's consider a scenario.
We documented this process through a behavior library (refer Table 1). In the core process of
adjusting the bed's configuration, the selection of the component to be moved is a pivotal step.
This may involve choosing a specific part of the bed or selecting a particular section for
adjustment. The challenge arose in finding a way to communicate this selection to users
non-verbally. Addressing this crucial question prompted us to rethink our design and come up
with ways to use a combination of movements, lights and sound to convey the choice to the
users. The functional embodiment also supplemented this effort.

