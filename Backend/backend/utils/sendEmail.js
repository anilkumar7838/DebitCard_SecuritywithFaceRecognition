const nodeMailer= require("nodemailer");

const sendEmail = async(options)=>{
    const transporter=nodeMailer.createTransport({
        host:process.env.SMPT_HOST,
        port:process.env.SMPT_PORT,
        service:process.env.SMPT_SERVICE,
        auth:{
            // simple mail transfer protocol
            user:process.env.SMPT_MAIL,
            pass:process.env.SMPT_PASSWORD,
        }
    })

    const mailOptions={
        from:process.env.SMPT_MAIL,
        to:options.reciever,
        subject:options.subject,
        text:options.message,
    }

    await transporter.sendMail(mailOptions);
}

module.exports=sendEmail;