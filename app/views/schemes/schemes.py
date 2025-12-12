from marshmallow import Schema, fields


class QuestionLikeSchema(Schema):
    question_id = fields.Integer(required=True)
    is_like = fields.Boolean(required=True)


class AnswerLikeSchema(Schema):
    answer_id = fields.Integer(required=True)
    is_like = fields.Boolean(required=True)


class AnswerCorrectSchema(Schema):
    answer_id = fields.Integer(required=True)
    is_correct = fields.Boolean(required=True)


# class GetQuestionsLikesSchema(Schema):
#     questions_ids = fields.List(fields.Integer(), required=True)