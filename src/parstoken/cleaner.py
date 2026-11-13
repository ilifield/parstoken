"""Text cleaning module for removing unwanted content.

Provides tools for stripping HTML tags, URLs, emails, emojis,
social media artifacts, and other noise from Persian text.
"""

import re
from typing import Optional


class TextCleaner:
    """Cleans text by removing unwanted elements like HTML, URLs, etc.
    
    Example:
        >>> cleaner = TextCleaner()
        >>> cleaner.clean("<p>سلام @user! https://example.com</p>")
        'سلام ! '
    """
    
    def __init__(
        self,
        remove_html: bool = True,
        remove_urls: bool = True,
        remove_emails: bool = True,
        remove_emojis: bool = False,
        remove_hashtags: bool = False,
        remove_mentions: bool = False,
        remove_phone_numbers: bool = False,
        remove_extra_newlines: bool = True,
    ):
        """Initialize the cleaner with configuration options.
        
        Args:
            remove_html: Remove HTML/XML tags.
            remove_urls: Remove web URLs.
            remove_emails: Remove email addresses.
            remove_emojis: Remove emoji characters.
            remove_hashtags: Remove hashtags (e.g. #topic).
            remove_mentions: Remove mentions (e.g. @user).
            remove_phone_numbers: Remove Iranian phone number patterns.
            remove_extra_newlines: Collapse 3+ newlines to 2.
        """
        self.remove_html_flag = remove_html
        self.remove_urls_flag = remove_urls
        self.remove_emails_flag = remove_emails
        self.remove_emojis_flag = remove_emojis
        self.remove_hashtags_flag = remove_hashtags
        self.remove_mentions_flag = remove_mentions
        self.remove_phone_numbers_flag = remove_phone_numbers
        self.remove_extra_newlines_flag = remove_extra_newlines
        
        # Pre-compile regex patterns
        self._html_re = re.compile(r'<[^>]+>')
        self._url_re = re.compile(
            r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\-.~:/?#\[\]@!$&\'()*+,;=%]*'
        )
        self._email_re = re.compile(
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        )
        self._hashtag_re = re.compile(r'#[\w\u0600-\u06FF]+')
        self._mention_re = re.compile(r'@[\w.]+')
        self._phone_re = re.compile(
            r'(?:\+98|0098|0)?9\d{9}'  # Iranian mobile numbers
            r'|(?:\+98|0098|0)\d{2,3}[-\s]?\d{7,8}'  # Landline numbers
        )
        self._extra_newlines_re = re.compile(r'\n{3,}')
        
        # Emoji pattern covering most emoji Unicode ranges
        self._emoji_re = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Misc Symbols and Pictographs
            "\U0001F680-\U0001F6FF"  # Transport and Map
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"  # Enclosed characters
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols Extended-A
            "\U00002600-\U000026FF"  # Misc symbols
            "\U0000FE00-\U0000FE0F"  # Variation Selectors
            "\U0000200D"             # Zero Width Joiner
            "\U00000023\U0000FE0F\U000020E3"  # Keycap #
            "]+",
            flags=re.UNICODE,
        )
    
    def clean(self, text: str) -> str:
        """Apply full cleaning pipeline to the text.
        
        Args:
            text: The text to clean.
            
        Returns:
            Cleaned text.
        """
        if not text:
            return text
        
        if self.remove_html_flag:
            text = self.strip_html(text)
        
        if self.remove_urls_flag:
            text = self.strip_urls(text)
        
        if self.remove_emails_flag:
            text = self.strip_emails(text)
        
        if self.remove_phone_numbers_flag:
            text = self.strip_phone_numbers(text)
        
        if self.remove_mentions_flag:
            text = self.strip_mentions(text)
        
        if self.remove_hashtags_flag:
            text = self.strip_hashtags(text)
        
        if self.remove_emojis_flag:
            text = self.strip_emojis(text)
        
        if self.remove_extra_newlines_flag:
            text = self._extra_newlines_re.sub('\n\n', text)
        
        return text
    
    def strip_html(self, text: str) -> str:
        """Remove HTML/XML tags from text.
        
        Args:
            text: Input text.
            
        Returns:
            Text without HTML tags.
        """
        return self._html_re.sub('', text)
    
    def strip_urls(self, text: str) -> str:
        """Remove URLs from text.
        
        Args:
            text: Input text.
            
        Returns:
            Text without URLs.
        """
        return self._url_re.sub('', text)
    
    def strip_emails(self, text: str) -> str:
        """Remove email addresses from text.
        
        Args:
            text: Input text.
            
        Returns:
            Text without email addresses.
        """
        return self._email_re.sub('', text)
    
    def strip_emojis(self, text: str) -> str:
        """Remove emoji characters from text.
        
        Args:
            text: Input text.
            
        Returns:
            Text without emojis.
        """
        return self._emoji_re.sub('', text)
    
    def strip_hashtags(self, text: str) -> str:
        """Remove hashtags from text.
        
        Args:
            text: Input text.
            
        Returns:
            Text without hashtags.
        """
        return self._hashtag_re.sub('', text)
    
    def strip_mentions(self, text: str) -> str:
        """Remove @mentions from text.
        
        Args:
            text: Input text.
            
        Returns:
            Text without mentions.
        """
        return self._mention_re.sub('', text)
    
    def strip_phone_numbers(self, text: str) -> str:
        """Remove Iranian phone numbers from text.
        
        Handles mobile numbers (09XXXXXXXXX) and landline numbers
        with various formats.
        
        Args:
            text: Input text.
            
        Returns:
            Text without phone numbers.
        """
        return self._phone_re.sub('', text)
