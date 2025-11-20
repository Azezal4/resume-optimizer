
# Table of Contents

1.  [I'm getting depressed customising my resume to every job I apply. I feel like my life is being wasted just on formatting. Let's do a simple math:](#org8834cfe):ATTACH:
    1.  [After a careful examination, I plan to go with plan B, i.e Making this thing portable.](#orgc6cf7f6)
2.  [Proof of concept](#orgd2df78f)
3.  [Starting with docker, I'm using arch, so installation and config of the docker doesn't seem to much. I just run](#org191ea68)
    1.  [Found something interesting on why docker need root previlages,   :ATTACH:x](#orgead5214)


<a id="org8834cfe"></a>

# I'm getting depressed customising my resume to every job I apply. I feel like my life is being wasted just on formatting. Let's do a simple math:     :ATTACH:

    // Consider 5 job application
    5 x 20 min(Resumes, cover letters, application) = 100 min
    // I've been applying for 3 months now so,
    100 x 30 = 3000 min (i.e 50 days sad 😒) damn.....  

So, My goal is to reduce this time to roughly 5 minutes which in turns gives me back my 15 minutes 😃.
The architecture in my mind:

![img](/home/ujjwal/Downloads/Untitled Diagram.drawio.png)


<a id="orgc6cf7f6"></a>

## After a careful examination, I plan to go with plan B, i.e Making this thing portable.


<a id="orgd2df78f"></a>

# Proof of concept


<a id="org191ea68"></a>

# Starting with docker, I'm using arch, so installation and config of the docker doesn't seem to much. I just run

    sudo pacman -S docker
    systemctl start/enable docker.serviceq

\*/ Note: The docker service is only accessible by root user so change in permission is necessary.

    sudo useradd docker // but most of the time user is already created
    sudo usermod -aG docker $USER // need to add the user to the docker group
    // check
    docker ps // should work


<a id="orgead5214"></a>

## Found something interesting on why docker need root previlages,   :ATTACH:x

-   docker runs KVM
    -   KVM being a hypervisor, needs the base level permission

Now, After spending 1 hour of debugging on why ollama is not being installed, i forgot yesterday exists. And Yes, yesterday yours truly tested ollama on my pc globally. Without any env or being containerized.
So what do we learn from this?

-   search for open port
-   check for any processes using that port
-   kill the damn port
-   previous installation also creats a container named ollma, so best of luck 👍.

After all of this, we still need to install `nvidia-container-toolkit` cause I have some gpu 😀.
Everything runs great on a containeraized environment.
![img](/home/ujjwal/Pictures/1.png)

