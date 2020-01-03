# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# author : strangestring
# github : https://github.com/strangestring

import time
import functools
import collections.abc


def singleton(cls):
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    
    return get_instance


@singleton
class HeadersRequired:
    """无headers也能得到完整信息"""
    pass


@singleton
class HeadersOptional:
    """无headers信息不完整或无法获得信息"""
    pass


class BaseAPI:
    def __init__(self, identifier, ):
        self.identifier = identifier


class TextAPI(BaseAPI):
    """目前仅ZhiHu.questions.log"""

    def __init__(self, identifier, ):
        super().__init__(identifier)


@functools.lru_cache(1000)  # 用此加速同款url处理速度
def _api_name(raw_name, api_name_separator):
    raw_name = raw_name.strip('_')
    return ''.join([
        f'{api_name_separator}{c.lower()}' if i and c.isupper() else c.lower()
        for i, c in enumerate(raw_name)])


class JsonAPI(BaseAPI):
    def __init__(self, identifier, ):
        super().__init__(identifier, )
        self.root_prefix = 'https://www.zhihu.com/api/v4'  # self.__object_prefix = None

    def url_maker(self, object_prefix: str, raw_api_name: str,
                  query_args: collections.abc.Iterable,
                  api_name_separator: str = '-', **kwargs) -> str:
        """
        url定制核心函数
        :param object_prefix: 'members' / 'questions'.etc
        :param raw_api_name: 'followers' / 'relations/mutuals'.etc
        :param query_args: ['is_following','comment_count'].etc
        :param api_name_separator: '-' / '_'
        :param kwargs: 'offset' / 'limit' / 'sort_by'
        :return: URL
        """

        path_fragments = [self.root_prefix, object_prefix, self.identifier]
        if (raw_api_name is not None) and (
                raw_api_name != '_Info'):  # info类API无此部分
            # raw_api_name = type(self).__name__
            # e.g. '_ColumnContributions' -> 'column-contributions'
            # attention: '_ConcernedUpvoters' -> 'concerned_upvoters'
            path_fragments.append(_api_name(raw_api_name, api_name_separator))
            ...
        query_fragments = []
        if query_args:
            query_fragments.append(f'include=data[*].{",".join(query_args)}')
            ...
        query_fragments.extend(
                [f'{param}={value}' for param, value in kwargs.items()])
        path_part = '/'.join(path_fragments)
        query_part = '&'.join(query_fragments)
        return '?'.join([path_part, query_part]) if query_part else path_part


class Pageable(JsonAPI):
    def __init__(self, identifier, ):
        super().__init__(identifier, )
        self.pageable = True


class UnPageable(JsonAPI):
    def __init__(self, identifier, ):
        super().__init__(identifier, )
        self.pageable = False


@singleton
class ZhiHu:

    def __init__(self):
        """
        Core of zhihu API
        """
        self.members = self._Members()
        self.articles = self._Articles()
        self.answers = self._Answers()
        self.questions = self._Questions()
        self.pins = self._Pins()
        self.topics = self._Topics()


    @singleton
    class _Members:

        def __init__(self):
            self.info = self._Info
            self.followees = self._Followees
            self.followers = self._Followers
            self.activities = self._Activities
            self.pins = self._Pins
            self.answers = self._Answers
            self.articles = self._Articles
            self.questions = self._Questions
            self.column_contributions = self._ColumnContributions
            self.favlists = self._Favlists
            self.following_columns = self._FollowingColumns
            self.following_topic_contributions = self._FollowingTopicContributions
            self.following_questions = self._FollowingQuestions
            self.following_favlists = self._FollowingFavlists
            self.marked_answers = self._MarkedAnswers
            self.included_articles = self._IncludedArticles
            self.mutuals = self._Mutuals

        class _Info(UnPageable):
            def __init__(self, url_token, query_args=None):
                """
                用户信息
            :param url_token:
            :param query_args:'allow_message','is_followed','is_following','description','is_org','is_blocking','employments','answer_count','follower_count','articles_count','gender','thanked_count','favorited_count','badge[?(type=best_answerer)].topics' ,etc.
            :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args)

        class _Followees(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None):
                """
                用户关注的人
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _Followers(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None):
                """
                用户的关注者
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _Activities(Pageable):
            def __init__(self, url_token, after_id=int(time.time()), limit=7,
                         query_args=None, desktop=True,
                         session_id=1099803331731554304):
                """
                Because of the high cost of obtaining full dynamics
                asynchronously, it is recommended to use this method
                only to determine the active state of the user in
                a certain period of time

                If you replace 'after_id with 'before_id'here
                the effect is the same as after_id=int(time.time)
                desktop=True seems have no effect

                param 'session_id' is removed.The original description is as follows: each logged-in user has a unique session_id,please fill in your own uid above,you may construct your own session_id pool
                :param url_token:
                :param after_id: another form of offset
                :param limit:
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=after_id,
                                          limit=limit, desktop=desktop,
                                          session_id=session_id)

        class _Pins(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None):
                """
                想法
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _Answers(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         sort_by='voteups'):
                """
                回答
                :param url_token:
                :param offset:
                :param limit:
                :param sort_by:'voteups'/'created'
                :param query_args:'is_normal','admin_closed_comment','reward_info',
                'is_collapsed','annotation_action','annotation_detail','collapse_reason',
                'collapsed_by','suggest_edit','comment_count','can_comment','content',
                'voteup_count','reshipment_settings','comment_permission','mark_infos',
                'created_time','updated_time','review_info','question','excerpt',
                'is_labeled','label_info','relationship.is_authorized','voting',
                'is_author','is_thanked','is_nothelp',
                'is_recognized;data[*].author.badge[?(type=best_answerer)].topics'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, sort_by=sort_by)

        class _Articles(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         sort_by='voteups'):
                """
                文章
                :param url_token:
                :param offset:
                :param limit:
                :param sort_by:'voteups'/'created'
                :param query_args:'comment_count','suggest_edit','is_normal',
                'thumbnail_extra_info','thumbnail','can_comment','comment_permission',
                'admin_closed_comment','content','voteup_count','created','updated',
                'upvoted_followees','voting','review_info','is_labeled',
                'label_info;data[*].author.badge[?(type=best_answerer)].topics'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, sort_by=sort_by)

        class _Questions(Pageable):
            def __init__(self, url_token, offset=0, limit=20,
                         query_args=None, ):
                """
                提问
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:'created','answer_count','follower_count','author','admin_closed_comment'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, )

        class _ColumnContributions(Pageable):
            def __init__(self, url_token, offset=0, limit=20,
                         query_args=None, ):
                """
                专栏
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:'column.intro','followers','articles_count'
                :return:
                """

                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, )

        class _Favlists(Pageable):
            def __init__(self, url_token, offset=0, limit=20,
                         query_args=None, ):
                """
                收藏夹
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:'updated_time','answer_count','follower_count','is_public'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, )

        class _FollowingColumns(Pageable):
            def __init__(self, url_token, offset=0, limit=20,
                         query_args=None, ):
                """
                关注的专栏
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:'intro','followers','articles_count'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, )

        class _FollowingTopicContributions(Pageable):
            def __init__(self, url_token, offset=0, limit=20,
                         query_args=None, ):
                """
                关注的话题(及在该话题下的回答数量(?))
                :param url_token:
                :param offset:
                :param limit:
                :param query_args: 'topic','introduction'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, )

        class _FollowingQuestions(Pageable):
            def __init__(self, url_token, offset=0, limit=20,
                         query_args=None, ):
                """
                关注的问题
                :param url_token:
                :param offset:
                :param limit:
                :param query_args: 'created','answer_count','follower_count','author'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, )

        class _FollowingFavlists(Pageable):
            def __init__(self, url_token, offset=0, limit=20,
                         query_args=None, ):
                """
                关注的收藏夹
                :param url_token:
                :param offset:
                :param limit:
                :param query_args: 'updated_time','answer_count','follower_count'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, )

        class _MarkedAnswers(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         sort_by='voteups'):
                """
                被收录回答
                :param url_token:
                :param offset:
                :param limit:
                :param sort_by:'voteups'/'created'
                :param query_args:'is_normal','admin_closed_comment','reward_info',
                'is_collapsed','annotation_action','annotation_detail','collapse_reason',
                'collapsed_by','suggest_edit','comment_count','can_comment','content',
                'voteup_count','reshipment_settings','comment_permission','mark_infos',
                'created_time','updated_time','review_info','question','excerpt',
                'is_labeled','label_info','relationship.is_authorized','voting',
                'is_author','is_thanked','is_nothelp',
                'is_recognized;data[*].author.badge[?(type=best_answerer)].topics'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, sort_by=sort_by)

        class _IncludedArticles(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         sort_by='voteups'):
                """
                被收录文章
                :param url_token:
                :param offset:
                :param limit:
                :param sort_by:'voteups'/'created'
                :param query_args:
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, sort_by=sort_by)

        class _Mutuals(Pageable):
            def __init__(self, url_token, offset=0, limit=10, query_args=None,
                         sort_by='voteups'):
                """
                我的关注中也关注TA的人
                :param url_token:
                :param offset:
                :param limit:
                :param sort_by:
                :param query_args:'answer_count','articles_count','gender','follower_count',
                'is_followed','is_following','badge[?(type=best_answerer)].topics'
                :return:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('members', 'realtions/mutuals',
                                          query_args, offset=offset,
                                          limit=limit, sort_by=sort_by)


    @singleton
    class _Articles:

        def __init__(self):
            self.info = self._Info
            self.likers = self._Likers
            self.concerned_upvoters = self._ConcernedUpvoters
            self.root_comments = self._RootComments
            self.comments = self._Comments

        class _Info(UnPageable):
            def __init__(self, article_id, query_args=None):
                """
                用户信息
            :param article_id:
            :param query_args:'allow_message','is_followed','is_following','description','is_org','is_blocking','employments','answer_count','follower_count','articles_count','gender','thanked_count','favorited_count','badge[?(type=best_answerer)].topics' ,etc.
            :return:
                """
                super().__init__(article_id, )
                self.url = self.url_maker('articles', type(self).__name__,
                                          query_args)

        class _Likers(Pageable):
            def __init__(self, article_id, offset=0, limit=20, query_args=None):
                """
                up_voters
                :param article_id:
                :param offset:
                :param limit:
                :param query_args:
                :return:
                """
                super().__init__(article_id, )
                self.url = self.url_maker('articles', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _ConcernedUpvoters(UnPageable):
            def __init__(self, article_id, query_args=None):
                """
                我的关注中的点赞者
                API限定至多查询5人,无法翻页
                :param article_id:
                :param query_args:
                """
                super().__init__(article_id, )
                self.url = self.url_maker('articles', type(self).__name__,
                                          query_args, api_name_separator='_', )

        class _RootComments(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         order='normal', status='open'):
                """
                二级结构评论
                e.g.'https://www.zhihu.com/api/v4/articles/37569973/root_comments?order=normal&limit=2&offset=2&status=open'
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                :param order: 强烈建议使用默认值
                :param status: 作用未知
                """
                super().__init__(url_token, )
                self.url = self.url_maker('articles', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, order=order,
                                          status=status)

        class _Comments(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         order='reverse', status='open'):
                """
                非结构化评论,'reverse'即'按时间排序'
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                :param order:
                :param status: 作用未知
                """
                super().__init__(url_token, )
                self.url = self.url_maker('articles', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, order=order,
                                          status=status)


    @singleton
    class _Answers:

        def __init__(self):
            self.info = self._Info
            self.voters = self._Voters
            self.concerned_upvoters = self._ConcernedUpvoters
            self.favlists = self._Favlists
            self.root_comments = self._RootComments
            self.comments = self._Comments

        class _Info(UnPageable):
            def __init__(self, answer_id, query_args=None):
                """
                回答信息
                :param answer_id:
                :param query_args:
                """
                super().__init__(answer_id, )
                self.url = self.url_maker('answers', type(self).__name__,
                                          query_args)

        class _Voters(Pageable):
            def __init__(self, answer_id, offset=0, limit=20, query_args=None):
                """
                点赞者
                :param answer_id:
                :param offset:
                :param limit:
                :param query_args: 'answer_count','articles_count','follower_count',
                'gender','is_followed','is_following','badge'
                :return:
                """
                super().__init__(answer_id, )
                self.url = self.url_maker('answers', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _ConcernedUpvoters(UnPageable):
            def __init__(self, answer_id, query_args=None):
                """
                我的关注中的点赞者
                :param answer_id:
                :param query_args:
                :return:
                """
                super().__init__(answer_id, )
                self.url = self.url_maker('answers', type(self).__name__,
                                          query_args, )

        class _Favlists(Pageable):
            def __init__(self, answer_id, offset=0, limit=20, query_args=None):
                """
                收录该回答的收藏夹
                :param answer_id:
                :param offset:
                :param limit:
                :param query_args:
                :return:
                """
                super().__init__(answer_id, )
                self.url = self.url_maker('answers', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _RootComments(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         order='normal', status='open'):
                """
                二级结构评论
                e.g.'https://www.zhihu.com/api/v4/articles/37569973/root_comments?order=normal&limit=2&offset=2&status=open'
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                :param order: 强烈建议使用默认值
                :param status: 作用未知
                """
                super().__init__(url_token, )
                self.url = self.url_maker('answers', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, order=order,
                                          status=status)

        class _Comments(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         order='reverse', status='open', ):
                """
                非结构化评论,'reverse'即'按时间排序'
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                :param order:
                :param status: 作用未知
                """
                super().__init__(url_token, )
                self.url = self.url_maker('answers', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, order=order,
                                          status=status)


    @singleton
    class _Questions:

        def __init__(self):
            self.info = self._Info
            self.log = self._Log
            self.followers = self._Followers
            self.concerned_followers = self._ConcernedFollowers
            self.answers = self._Answers
            self.collapsed_answers = self._CollapsedAnswers
            self.root_comments = self._RootComments
            self.comments = self._Comments
            self.similar_questions = self._SimilarQuestions

        class _Info(UnPageable):
            def __init__(self, url_token, query_args=None, ):
                """
                信息
                :param url_token:
                :param query_args:
                """
                super().__init__(url_token, )
                self.url = self.url_maker('questions', type(self).__name__,
                                          query_args)

        class _Log(TextAPI):
            def __init__(self, question_id, ):
                super().__init__(question_id)
                self.url = f'https://www.zhihu.com/question/{question_id}/log'

        class _Followers(Pageable):
            def __init__(self, question_id, offset=0, limit=20,
                         query_args=None, ):
                """
                问题的关注者
                :param question_id:
                :param offset:x
                :param limit:
                :param query_args:'gender','answer_count','articles_count',
                'follower_count','is_following','is_followed'
                :return:
                """
                super().__init__(question_id, )
                self.url = self.url_maker('questions', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _ConcernedFollowers(Pageable):
            def __init__(self, question_id, offset=0, limit=20,
                         query_args=None, ):
                """
                我的关注中的关注者
                :param question_id:
                :param offset:
                :param limit:
                :param query_args:
                :return:
                """
                super().__init__(question_id, )
                self.url = self.url_maker('questions', type(self).__name__,
                        query_args, api_name_separator='_', offset=offset,
                        limit=limit)

        class _Answers(Pageable):
            def __init__(self, question_id, offset=0, limit=20, query_args=None,
                    sort_by='default', ):
                """
                问题下的回答
                :param question_id:
                :param offset:
                :param limit:
                :param sort_by: 'default','updated'
                :param query_args: 'is_normal','admin_closed_comment','reward_info',
                'is_collapsed','annotation_action','annotation_detail',
                'collapse_reason','is_sticky','collapsed_by','suggest_edit',
                'comment_count','can_comment','content','editable_content',
                'voteup_count','reshipment_settings','comment_permission',
                'created_time','updated_time','review_info','relevant_info',
                'question','excerpt','relationship.is_authorized','is_author',
                'voting','is_thanked','is_nothelp','is_labeled','is_recognized',
                'paid_info','paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count','badge[*].topics'
                :return:
                """
                super().__init__(question_id, )
                self.url = self.url_maker('questions', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, sort_by=sort_by)

        # todo:尝试实现更复杂的query_args定制

        class _CollapsedAnswers(Pageable):
            def __init__(self, question_id, offset=0, limit=20,
                    query_args='is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
                    sort_by='default', ):
                """
                问题下被折叠的回答
                :param question_id:
                :param offset:
                :param limit:
                :param sort_by:
                :param query_args:
                :return:
                """
                super().__init__(question_id, )
                self.url = self.url_maker('questions', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, sort_by=sort_by)

        class _RootComments(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         order='normal', status='open', ):
                """
                二级结构评论
                e.g.'https://www.zhihu.com/api/v4/articles/37569973/root_comments?order=normal&limit=2&offset=2&status=open'
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                :param order: 强烈建议使用默认值
                :param status: 作用未知
                """
                super().__init__(url_token, )
                self.url = self.url_maker('questions', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, order=order,
                                          status=status)

        class _Comments(Pageable):
            def __init__(self, url_token, offset=0, limit=20, query_args=None,
                         order='reverse', status='open', ):
                """
                非结构化评论,'reverse'即'按时间排序'
                :param url_token:
                :param offset:
                :param limit:
                :param query_args:
                :param order:
                :param status: 作用未知
                """
                super().__init__(url_token, )
                self.url = self.url_maker('questions', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, order=order,
                                          status=status)

        class _SimilarQuestions(UnPageable):
            def __init__(self, question_id, limit=5, query_args=None, ):
                """
                相似问题
                :param question_id:
                :param limit:
                :param query_args:
                """
                super().__init__(question_id, )
                self.url = self.url_maker('questions', type(self).__name__,
                                          query_args, limit=limit)


    @singleton
    class _Pins:

        def __init__(self):
            self.info = self._Info
            self.actions = self._Actions
            self.comments = self._Comments

        class _Info(UnPageable):
            def __init__(self, pin_id, query_args=None):
                """
                想法信息
                :param pin_id:
                :param query_args:
                """
                super().__init__(pin_id, )
                self.url = self.url_maker('pins', type(self).__name__,
                                          query_args)

        class _Actions(Pageable):
            def __init__(self, pin_id, offset=0, limit=20, query_args=None):
                """
                想法转发及鼓掌名单
                :param pin_id:
                :param offset:
                :param limit:
                :param query_args:
                :return:
                """
                super().__init__(pin_id, )
                self.url = self.url_maker('pins', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _Comments(Pageable):
            def __init__(self, pin_id, offset=0, limit=20, query_args=None,
                         order='reverse', status='open'):
                """
                非结构化评论,'reverse'即'按时间排序'
                :param pin_id:
                :param offset:
                :param limit:
                :param query_args:
                :param order:
                :param status: 作用未知
                """
                super().__init__(pin_id, )
                self.url = self.url_maker('pins', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit, order=order,
                                          status=status)


    @singleton
    class _Topics:

        def __init__(self):
            self.info = self._Info
            self.followers = self._Followers
            self.timeline_question = self._TimelineQuestion

        class _Info(UnPageable):
            def __init__(self, topic_id, query_args=None):
                """
                想法信息
                :param topic_id:
                :param query_args:
                """
                super().__init__(topic_id, )
                self.url = self.url_maker('topics', type(self).__name__,
                                          query_args)

        class _Followers(Pageable):
            def __init__(self, topic_id, offset=0, limit=20, query_args=None):
                """
                关注者
                :param topic_id:
                :param offset:
                :param limit:
                :param query_args:'gender','answer_count','articles_count',
                'follower_count','is_following','is_followed'
                :return:
                """
                super().__init__(topic_id, )
                self.url = self.url_maker('topics', type(self).__name__,
                                          query_args, offset=offset,
                                          limit=limit)

        class _TimelineQuestion(Pageable):
            def __init__(self, topic_id, offset=0, limit=10, query_args=None):
                """

                :param topic_id:
                :param offset:
                :param limit:
                :param query_args:'visit_count'
                :return:
                """
                '''
                            {self.url_prefix}/20009759/feeds/timeline_question
                ?include=
                .target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;

                .target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;

                .target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;

                .target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;

                data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;

                data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;

                data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;

                data[?(target.type=question)].target.annotation_detail,comment_count;

                &limit=10&offset=35
                            '''
                # The customization of this thing is very complex, suggest to
                # modify here directly
                super().__init__(topic_id, )
                # f'{self.url_prefix}/{topic_id}/feeds/timeline_question?limit={limit}&offset={offset}'
                self.url = self.url_maker('topics', 'feeds/timeline_question',
                        query_args, api_name_separator='_', offset=offset,
                        limit=limit)


    @singleton
    class _Report:

        @staticmethod
        def reports(page=1):
            return f'https://www.zhihu.com/api/v4/reports?page={page}'


if __name__ == '__main__':
    # 使用示例
    zhi = ZhiHu()
    __member = zhi.members
    b = zhi.members
    print(id(__member) == id(b))
    # print(member.__dir__()[:17])
    __funcs = []
    __test_url_token = 'strangestring'
    __funcs.append(__member.info(__test_url_token,
                                 query_args=['is_following', 'voteup_count']))
    __funcs.append(__member.followees(__test_url_token, 0, 3,
                                      query_args=['is_following',
                                                  'voteup_count']))
    __funcs.append(__member.followers(__test_url_token, 0, 3,
                                      query_args=['is_following',
                                                  'voteup_count']))
    __funcs.append(__member.activities(__test_url_token, ))
    __funcs.append(__member.pins(__test_url_token, ))
    __funcs.append(__member.answers(__test_url_token, sort_by='voteups'))
    __funcs.append(__member.answers(__test_url_token, sort_by='created'))
    __funcs.append(__member.articles(__test_url_token, sort_by='voteups'))
    __funcs.append(__member.articles(__test_url_token, sort_by='created'))
    __funcs.append(__member.questions(__test_url_token, ))
    __funcs.append(__member.column_contributions(__test_url_token))
    __funcs.append(__member.favlists(__test_url_token))

    for __ in __funcs:
        print(f'{__.url}\n')
