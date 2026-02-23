from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:mypassword@localhost:3306/content_moderation"
engine = create_engine(DATABASE_URL)


class Comment(BaseModel):
    text: str


# ----------------------------
# Moderation Rule Definitions
# ----------------------------

violent_threats = ["kill", "murder", "die", "execute", "hang"]
hate_speech = ["nigga", "racist", "terrorist"]
direct_abuse = [
    "idiot", "stupid", "moron", "useless",
    "fraud", "scam", "corrupt",
    "garbage", "disgusting"
]
profanity = ["fuck", "shit", "bitch", "asshole", "motherfucker"]
mass_negativity = [
    "worst", "flop", "boycott", "ban",
    "bad", "disaster", "hate",
    "dislike", "overrated", "waste"
]


@app.post("/analyze")
def analyze_comment(comment: Comment):
    text_input = comment.text.lower()
    toxicity_score = 0

    # Weighted scoring
    for word in violent_threats:
        if word in text_input:
            toxicity_score += 4

    for word in hate_speech:
        if word in text_input:
            toxicity_score += 3

    for word in direct_abuse:
        if word in text_input:
            toxicity_score += 2

    for word in profanity:
        if word in text_input:
            toxicity_score += 1

    for word in mass_negativity:
        if word in text_input:
            toxicity_score += 1

    # Severity logic (priority based)
    if any(word in text_input for word in violent_threats):
        severity_category = "Violent Threat"
    elif any(word in text_input for word in hate_speech):
        severity_category = "Hate Speech"
    elif any(word in text_input for word in direct_abuse):
        severity_category = "Direct Abuse"
    elif any(word in text_input for word in profanity):
        severity_category = "Profanity"
    elif any(word in text_input for word in mass_negativity):
        severity_category = "Mass Negativity"
    else:
        severity_category = "Neutral"

    is_flagged = severity_category != "Neutral"

    # Insert into DB
    with engine.connect() as connection:
        connection.execute(
            text("""
                INSERT INTO comments 
                (comment, toxicity_score, severity_category, moderation_status, is_flagged)
                VALUES (:comment, :score, :severity, :status, :flagged)
            """),
            {
                "comment": comment.text,
                "score": toxicity_score,
                "severity": severity_category,
                "status": "Pending",
                "flagged": is_flagged
            }
        )
        connection.commit()

    return {
        "comment": comment.text,
        "toxicity_score": toxicity_score,
        "severity_category": severity_category,
        "is_flagged": is_flagged,
        "moderation_status": "Pending"
    }


@app.get("/comments")
def get_all_comments():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM comments"))
        rows = result.fetchall()

    return [
        {
            "id": row[0],
            "comment": row[1],
            "toxicity_score": row[2],
            "severity_category": row[3],
            "created_at": row[4],
            "moderation_status": row[5],
            "is_flagged": row[6]
        }
        for row in rows
    ]


@app.get("/comments/flagged")
def get_flagged_comments():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM comments WHERE is_flagged = TRUE")
        )
        rows = result.fetchall()

    return [
        {
            "id": row[0],
            "comment": row[1],
            "toxicity_score": row[2],
            "severity_category": row[3],
            "created_at": row[4],
            "moderation_status": row[5],
            "is_flagged": row[6]
        }
        for row in rows
    ]


@app.put("/comments/{comment_id}/approve")
def approve_comment(comment_id: int):
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE comments SET moderation_status = 'Approved' WHERE id = :id"),
            {"id": comment_id}
        )
        connection.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Comment not found")

    return {"message": "Comment approved"}


@app.put("/comments/{comment_id}/reject")
def reject_comment(comment_id: int):
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE comments SET moderation_status = 'Rejected' WHERE id = :id"),
            {"id": comment_id}
        )
        connection.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Comment not found")


    return {"message": "Comment rejected"}
